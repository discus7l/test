######----------------- Original Script ----------------######
# import sheetControl
# response = sheetControl.myFunction()
# print(response)

######------------------- In folder --------------------######
# from locPack import sheetControl
# response = sheetControl.myFunction()
# print(response)

######------------ In folder /w __init__.py ------------######
# With init.py we can call the function within the module within the package in short calls
# virtually skipping the module name
# "package.function" rather than "package.module.function"
# We can also keep the import statement short, if that matters
# "import locPack" rather than "from locPack inport sheetControl"
# REF https://stackoverflow.com/questions/1944569/how-do-i-write-good-correct-package-init-py-files

# __init__.py content
# from locPack.sheetControl import myFunction as func

# Debian keeps site-packages in a strange place
# Below is the location in Debian
# /usr/local/lib/python3.9/dist-packages

import locPack
response = locPack.func()
print(response)
