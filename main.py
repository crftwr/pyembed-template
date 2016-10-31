﻿import os
import sys


if 1:
    import importlib.abc
    
    class CustomPydFinder(importlib.abc.MetaPathFinder):
        def find_module( self, fullname, path=None ):
            exe_path = os.path.split(sys.argv[0])[0]
            pyd_filename_body = fullname.split(".")[-1]
            pyd_fullpath = os.path.join( exe_path, "lib", pyd_filename_body + ".pyd" )
            if os.path.exists(pyd_fullpath):
                for importer in sys.meta_path:
                    if isinstance(importer, self.__class__):
                        continue
                    loader = importer.find_module( fullname, None)
                    if loader:
                        return loader

    sys.meta_path.append(CustomPydFinder())


import ckit
from ckit.ckit_const import *

ckit.registerWindowClass( "CkitTest" )

ckit.setTheme( "black", {} )

class Test1( ckit.TextWindow ):

    def __init__(self):
        
        ckit.TextWindow.__init__(
            self,
            x=20, 
            y=10, 
            width=80, 
            height=24,
            title_bar = True,
            title = "Ckit Test",
            sysmenu=True,
            activate_handler = self.onActivate,
            size_handler = self.onSize,
            close_handler = self.onClose,
            keydown_handler = self.onKeyDown,
            keyup_handler = self.onKeyUp,
            char_handler = self.onChar,
            )

        self.putString( 0, 0, 20, 1, ckit.Attribute( fg=(255,255,255), bg=(0,0,0) ), "Hello World!" )

    def onActivate( self, active ):
        print( "onActivate", active )

    def onSize( self, width, height ):
        print( "onSize" )
        self.putString( 0, 0, 20, 1, ckit.Attribute( fg=(255,255,255), bg=(0,0,0) ), " %d, %d     " % (width, height) )
        self.putString( 0, 1, 20, 1, ckit.Attribute( fg=(50,50,50), bg=(200,200,200) ), " 幅  高 " )

    def onClose(self):
        print( "onClose" )
        self.quit()

    def onKeyDown( self, vk, mod ):
        print( "onKeyDown", vk, mod )
        if vk==VK_RETURN:
            rect = self.getWindowRect()
            test2 = Test2( (rect[0]+rect[2])//2, (rect[1]+rect[3])//2, self.getHWND() )
            self.enable(False)
            test2.messageLoop()
            self.enable(True)
            self.activate()
            test2.destroy()
            
        elif vk==VK_D:
            
            string_list = [
                "Candidate1",
                "Candidate2",
                "Candidate3",
            ]
            
            def candidate_String( update_info ):

                candidates = []

                for s in string_list:
                    if s.lower().startswith( update_info.text.lower() ):
                        candidates.append( s )

                return candidates, 0
        
            dialog = ckit.Dialog( self, "DialogTest", items=[
                ckit.Dialog.StaticText(0,"StaticText1"),
                ckit.Dialog.StaticText(0,""),
                ckit.Dialog.Edit( "dialog_edit1", 4, 40, "Edit1", "default value" ),
                ckit.Dialog.StaticText(0,""),
                ckit.Dialog.Edit( "dialog_edit2", 4, 40, "Edit2", "", candidate_handler=candidate_String ),
                ckit.Dialog.StaticText(0,""),
                ckit.Dialog.CheckBox( "dialog_checkbox1", 4, "CheckBox1", False ),
                ckit.Dialog.CheckBox( "dialog_checkbox2", 4, "CheckBox2", True ),
                ckit.Dialog.StaticText(0,""),
                ckit.Dialog.StaticText(0,"Choice"),
                ckit.Dialog.StaticText(0,""),
                ckit.Dialog.Choice( "dialog_choice1", 4, "Choice1", [ "Option1", "Option2", "Option3" ], 1 ),
                ckit.Dialog.Choice( "dialog_choice2", 4, "Choice2", [ "選択１", "選択２", "選択３" ], 1 ),
            ])
            dialog.messageLoop()
            result = dialog.getResult()
            dialog.destroy()
            
            print(result)

    def onKeyUp( self, vk, mod ):
        print( "onKeyUp", vk, mod )

    def onChar( self, ch, mod ):
        print( "onChar", ch, mod )


class Test2( ckit.Window ):

    def __init__(self,x,y,parent_window):
        
        ckit.Window.__init__(
            self,
            x=x, 
            y=y, 
            width=80, 
            height=24,
            origin= ORIGIN_X_CENTER | ORIGIN_Y_CENTER,
            parent_window=parent_window,
            resizable = False,
            minimizebox = False,
            maximizebox = False,
            activate_handler = self.onActivate,
            close_handler = self.onClose,
            keydown_handler = self.onKeyDown,
            keyup_handler = self.onKeyUp,
            char_handler = self.onChar,
            )

    def onActivate( self, active ):
        print( "onActivate", active )

    def onClose(self):
        print( "onClose" )
        self.quit()

    def onKeyDown( self, vk, mod ):
        print( "onKeyDown", vk, mod )
        if vk==VK_ESCAPE:
            self.quit()

    def onKeyUp( self, vk, mod ):
        print( "onKeyUp", vk, mod )

    def onChar( self, ch, mod ):
        print( "onChar", ch, mod )


test1 = Test1()

print( "before messageLoop" )

test1.messageLoop()

print( "after messageLoop" )

test1.destroy()

