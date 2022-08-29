# Cloudifier
#### Description:
This program illustrates the grouping of pixels that touch eachother horizontally or vertically, just like the movement of a rook across a chessboard. The resulting output are pictures of which the first one displays horizontally touching pixels in each row having the same color (called "cloudlines"). The second picture shows the result after those horizontal lines have been merged if they are connected vertically. In this resulting second picture all pixels sharing a vertical or horizontal border have the same color.

#### Installation:
The program requires Python 3 and two libraries: Pillow and Mathplotlib.

For installation Python offers the option to use virtual environments (venv). In this way the extra packages needed are installed locally and will not be permanently integrated into your system.

You will need the "requirements.txt" file from the project folder.

1. Open a Terminal window and navigate to the project folder. Create a virtual environment:

    ```$ python3 -m venv env```

    (will create a new folder)

2. You will now activate the venv by:

    ```$ source env/bin/activate```

3. In order to check if the previous step was done correctly you can now type:

    ```$ which python```

    This should give something like "/cloudifier/env/bin/python" and **not** "/usr/bin/python"

4. Install the packages from the requirements:

    ```$ pip3 install -r requirements.txt```

    Installation is now complete.

5. Deactivate the venv:

    ```$ deactivate```

6. In order to check if the previous step was done correctly you can now type:

    ```$ which python```

    This should give something like "/usr/bin/python" and **not** "/cloudifier/env/bin/python"

#### Use:
How to run cloudifier with Python's venv:

1. Open Terminal in project folder
2. Activate venv and run application:

    ```$ source env/bin/activate && python3 cloudifier.py```

Or, depending on your default Python version: replace "python3" by "python"

