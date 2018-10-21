import face_recognition
import pickle
import cv2
import os
import telegram
from imutils import paths
from scripts import botManag

# Unfortunately a global variable...
image_caption = None

# To avoid mistype in the script
received_folder = "received"
output_folder = "output"
dataset_folder = "dataset"

def saveImage(bot, update):
    '''
    Save the received image on received folder 
    '''

    # Create a file name path based on date it was received
    file_name = botManag.getFolderPath(folder_name = received_folder) + \
                botManag.makeFileName(fileDate = update.message.date) + \
                ".jpg"

    # Store the person's name
    global image_caption
    image_caption = update.message.caption
    
    # Download the file
    file_id = update.message.photo[-1].file_id
    newFile = bot.get_file(file_id)
    newFile.download(file_name)

def identifyPhoto(bot, update):
    '''
    Identify the people/objects at the last given image.
    '''

    chat_id = update.message.chat_id
    file_name = botManag.lastFileOnFolder(received_folder)
    file_path = botManag.getFolderPath(received_folder) + file_name
    output_archive = botManag.getFolderPath(output_folder) + file_name
    pickle_path = botManag.getScriptPath() + "encodings.pickle"

	# Load the known faces and embeddings.
    data = pickle.loads(open(pickle_path, "rb").read())

    # Load the input image and convert it from BGR to RGB.
    image = cv2.imread(file_path)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

	# Detect the (x, y)-coordinates of the bounding boxes corresponding
	# to each face in the input image, then compute the facial embeddings
	# for each face.
    boxes = face_recognition.face_locations(rgb, model="cnn")
    encodings = face_recognition.face_encodings(rgb, boxes)

	# Initialize the list of names for each face detected
    names = []

	# Loop over the facial embeddings
    for encoding in encodings:
        # Attempt to match each face in the input image to our known
        # encodings.
        matches = face_recognition.compare_faces(data["encodings"], encoding)
        name = "Unknown"

        # Check to see if we have found a match.
        if True in matches:

            # Find the indexes of all matched faces then initialize a
            # dictionary to count the total number of times each face
            # was matched.
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}

			# Loop over the matched indexes and maintain a count for
			# each recognized face face.
            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1

            # Determine the recognized face with the largest number of
            # votes (note: in the event of an unlikely tie Python will
            # select first entry in the dictionary).
            name = max(counts, key = counts.get)
	
        # Update the list of names.
        names.append(name)

    # Loop over the recognized faces.
    for ((top, right, bottom, left), name) in zip(boxes, names):

        # draw the predicted face name on the image
        cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
        y = top - 15 if top - 15 > 15 else top + 15
        cv2.putText(image, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
	
    # Save the file and send it to the chat. 
    cv2.imwrite(output_archive, image)
    bot.send_photo(chat_id = chat_id, photo = open(output_archive, 'rb'))

def generatePickles(bot, update):

    dataset_path = botManag.getFolderPath(dataset_folder)
    pickle_path = botManag.getScriptPath()

    # Grab the paths to the input images in our dataset.
    imagePaths = list(paths.list_images(dataset_path))

    # Initialize the list of known encodings and known names.
    knownEncodings = []
    knownNames = []

    # Loop over the image paths.
    for (i, imagePath) in enumerate(imagePaths):
	    # Extract the person name from the image path.
	    print("[INFO] processing image {}/{}".format(i + 1,
		    len(imagePaths)))
	    name = imagePath.split(os.path.sep)[-2]

	    # Load the input image and convert it from RGB (OpenCV ordering)
	    # to dlib ordering (RGB).
	    image = cv2.imread(imagePath)
	    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

	    # Detect the (x, y)-coordinates of the bounding boxes
	    # corresponding to each face in the input image.
	    boxes = face_recognition.face_locations(rgb, model="cnn")

	    # Compute the facial embedding for the face.
	    encodings = face_recognition.face_encodings(rgb, boxes)

	    # Loop over the encodings.
	    for encoding in encodings:
		    # Add each encoding + name to our set of known names and encodings.
		    knownEncodings.append(encoding)
		    knownNames.append(name)

    # Dump the facial encodings + names to disk.
    print("[INFO] serializing encodings...")
    data = {"encodings": knownEncodings, "names": knownNames}
    f = open((pickle_path + "encodings.pickle"), "wb")
    f.write(pickle.dumps(data))
    f.close()

    # Feedback to chat
    chat_id = update.message.chat_id
    message = "Pickles succesfully generated!"
    bot.sendMessage(chat_id = chat_id, text = message)
    
def registerName(bot, update):

    chat_id = update.message.chat_id
    username = update.message.from_user.first_name
    
    # If the sent image has no caption, send a feedback to the user.
    if (image_caption == None):
        message = "Please write his/her name on the image's caption and send it again"
        bot.sendMessage(chat_id = chat_id, text = message)
    
    # If the sent image has a caption, process it.
    else:

        # Substitute the spaces for underscores and make it in lower case.
        subfolder_name = image_caption.replace(" ","_")
        subfolder_name = subfolder_name.lower()
    
        # Move the sent image from received to dataset folder
        old_path = botManag.getFolderPath(received_folder) + \
                    botManag.lastFileOnFolder(received_folder)
        new_path = botManag.getFolderPath(dataset_folder + "/" + subfolder_name) + \
                    botManag.lastFileOnFolder(received_folder)
        botManag.moveFile(from_path = old_path, to_path = new_path)

        # Send a feedback to the chat
        message = "Registered!"
        bot.sendMessage(chat_id = chat_id, text = message)

# If this file was run directly, exit leaving a message.
if __name__ == "__main__":
    print("This script is not the main script to run.\n")
    print("Please check the documents.\n")
    exit()