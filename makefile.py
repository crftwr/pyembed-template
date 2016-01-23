
import os
import shutil
import zipfile
import py_compile


def compilePythonRecursively( src, dst ):

    directory_black_list = [
        "site-packages",
        "test",
        "tests",
        "idlelib",
    ]
    
    for root, dirs, files in os.walk( src ):

        for directory_to_remove in directory_black_list:
            if directory_to_remove in dirs:
                dirs.remove(directory_to_remove)

        for filename in files:
            if filename.endswith(".py"):
                src_filename = os.path.join(root,filename)
                dst_filename = os.path.join(dst+root[len(src):],filename+"c")
                print("compile", src_filename, dst_filename )
                py_compile.compile( src_filename, dst_filename, optimize=2 )


def createZip( zip_filename, items ):
    z = zipfile.ZipFile( zip_filename, "w", zipfile.ZIP_DEFLATED, True )
    for item in items:
        if os.path.isdir(item):
            for root, dirs, files in os.walk(item):
                for f in files:
                    f = os.path.normpath(os.path.join(root,f))
                    print( f )
                    z.write(f)
        else:
            print( item )
            z.write(item)
    z.close()


# compile python source files
if 1:
    compilePythonRecursively( "c:/Python35/Lib", "build/Lib" )
    compilePythonRecursively( "c:/Python35/Lib/site-packages/PIL", "build/Lib/PIL" )
    compilePythonRecursively( "../ckit", "build/Lib/ckit" )
    compilePythonRecursively( "../pyauto", "build/Lib/pyauto" )

# archive python compiled files
if 1:
    os.chdir("build/Lib")
    createZip( "../../library.zip", "." )
    os.chdir("../..")

# copy DLLs
if 1:
    if os.path.exists("lib"):
        shutil.rmtree("lib")

    shutil.copy( "c:/Python35/python35.dll", "python35.dll" )

    shutil.copytree( "c:/Python35/DLLs", "lib", ignore=shutil.ignore_patterns("*.pdb","*_d.pyd","*.ico","*.lib") )

    shutil.copy( "c:/Python35/Lib/site-packages/PIL/_imaging.cp35-win32.pyd", "lib/_imaging.pyd" )

    shutil.copy( "../ckit/ckitcore.pyd", "lib/ckitcore.pyd" )
    shutil.copy( "../pyauto/pyautocore.pyd", "lib/pyautocore.pyd" )

