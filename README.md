# Installation 

Just `pip install shelldoc`

# Usage 

```
usage: shelldoc [-h] -f FILES [FILES ...] [-d DEST]

Generate documentation from shell script

optional arguments:
  -h, --help            show this help message and exit
  -f FILES [FILES ...], --files FILES [FILES ...]
                        Files to generate documentation from
  -d DEST, --dest DEST  Directory to generate documentation in. ./docs by default
```
# Specifications

This documentation generation tool is based on [Google Shell Style Guide](https://google.github.io/styleguide/shellguide.html)

For example : 

```bash
#######################################
# Get configuration directory.
# Globals:
#   SOMEDIR
# Arguments:
#   None
# Outputs:
#   Writes location to stdout
# See: 
#   https://stackoverflow.com/questions/59895/getting-the-source-directory-of-a-bash-script-from-within
#   del_thing
#######################################
```

The following parameters are available :
- Globals
- Arguments
- Outputs
- Returns 
- See
- Raises

Also, the `TODO` are parsed.