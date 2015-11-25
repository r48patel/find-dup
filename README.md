# Find Duplicates
This script can be used to find any duplicate files. 

## Available Options
`--location` 
- Description: The root level location where to start the search.
- Type: String
- Default: The working directory of script.
- Example: `python find_dup.py --location some/root/location/`

`--custom-locations` 
- Description: List of custom location to check.
- Type: list (space separated parameter values)
- Example: `python find_dup.py --custom-locations location/one/ location/two/`

`--levels`
- Description: How many levels to check from the root level
- Type: Integer
- Default: 1 (only check root folder)
- Example: `python find_dup.py --location some/location --levels 2`

`--action`
- Description: What actions to take when duplicate files are found
- Type: String
- Choices: 
    + dry_run
    + rename
    + delete
- Default: dry_run

`--type`
- Description: Default list of different extension for certain types of file
- Type: String
- Choices:
    + pictures => ['png', 'jpeg', 'dng', 'NEF', 'jpg']
    + movies => ['mov, mp4, wmv', 'avi', 'mpg']

`--only-extension`
- Description: Only look at files with given extensions.
- Type: List
- Example: `python find_dup.py --location some/location --only-extensions exe1 exe2 pdf`

`--exclude-extensions`
- Description: Do not look at file with given extensions.
- Type: List
- Example: `python find_dup.py --location some/location --only-extensions mov mp4`

`--delete-empty-folders`
- Description: If there are no files in the folder, after either deleting or renaming,  
- Type: Boolean
- Default: False
- Example: `python finde_dup.py --location some/location --delete-empty-folders`

##Usage
- Base directory search (will not include any subdirectories)
    + `python find_dup.py --location some/location`
    + `python find_dup.py --location some/location --level=1`
    + Search current directory
        * `python find_dup.py`
    + Search current directory and delete empty folders
        * `python find_dup.py --delete-empty-folders`

- Include subdirectories (upto N level)
    + `pyhton find_dup.py -`


##Requirement
Following packages are required for this script to run. Instruction on how to install packages is below.
- enum34

##Installint Python packages
###Windows
1. Add python to `path` via cmd line

>If you already have python in your path, skip to step 2.

```
D:\>set path=%path%;D:\Python27
```
> Typically Python file are under 'C:\Python27'. Make sure to check your location.

2. Install pip by following these [instructions](https://pip.pypa.io/en/latest/installing/)

>If you already have pip installed, skip to step 3.

3. Install packages via pip

```
$ pip install enum34
```

To use requirement.txt

```
$ pip install -r requirement.txt
```

###Mac
1. Install Homebrew by following these [instrictions](http://brew.sh/)

>If you already have homebrew installed, skip to step 2.

2. Install pip

>if you already have python/pip installed, skip to step 3.

```
$ brew install python
```

3. Install pacakges via pip
```
$ pip install enum34
```

To use requirement.txt

```
$ pip install -r requirement.txt
```
