import TemplateMakerRaspi as tm
import Fotocamera as fc
import TemplateMatching_IMG_folder as match
import videocamera as videocam

command = input("Geef input: ")

if command == "foto":
    fc.makePhoto()
    print("foto made")
    
elif command == "make":
    tm.makeTemplate()
    print("template made")
    
elif command == "match":
    match.matchTemplates()
    print("matching done")
    
elif command == "video":
    print("start video recording")
    videocam.video_on()
    
