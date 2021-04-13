import win32com.client

def run():
    try:
        Application = win32com.client.Dispatch("PowerPoint.Application")
        Presentation = Application.Activepresentation
        return Presentation
    except:
        return -1

def nextslide(Presentation, next_slide):
    try:
        if(next_slide == 0):
            pass
        else:
            for i in range(next_slide):
                Presentation.SlideShowWindow.View.Next()
        return 1
    except:
        print("End of slide show reached")
        return -1
