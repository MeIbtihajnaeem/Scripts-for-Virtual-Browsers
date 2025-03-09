from server import ImageServer

port = 5800
imageServer = ImageServer(port=5801,image_path="assets/screenshot_5800.png",host="localhost")
imageServer.run_server()