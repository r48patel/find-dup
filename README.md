# Find Duplicates
This script can be used to find any duplicate files. 

## Available Options
`location` 
- Description: The root level location where to start the search.
- Type: String
- Default: The working directory of script.
- Example: `python find_dup.py --location some/root/location/`

`custom-locations` 
- Description: List of custom location to check.
- Type: list (space separated parameter values)
- Example: `python find_dup.py --custom-locations location/one/ location/two/`

`levels`
- Description: How many levels to check from the root level
- Type: Integer
- Default: 1 (only check root folder)
- Example: `python find_dup.py --location some/location --levels 2`

`action`
- Description: What actions to take when duplicate files are found
- Type: String
- Choices: 
    + dry_run
    + rename
    + delete
- Default: dry_run

`type`
- Description:
- Type:

`only-extension`
- Description:
- Type:

`exclude-extensions`
- Description:
- Type:

`delete-empty-folders`
- Description:
- Type:

##Usage

##Requirement


###Installing Python packages on Windows
1. Add python to `path` via cmd line

```
D:\>set path=%path%;D:\Python27
```
> Typically Python file are under 'C:\Python27'. Make sure to check your location.
	
2. Instal pip. Follow instructions [here](https://pip.pypa.io/en/latest/installing/)

3. Install packages via pip

```
$ pip install enum
```

To use requirement.txt

```
$ pip install -r requirement.txt
```