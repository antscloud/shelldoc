#!/bin/bash
#
# Perform hot backups of Oracle databases.
# And so on ...


#######################################
# Cleanup files from the backup directory.
# Globals:
#   BACKUP_DIR
#   ORACLE_SID
# Arguments:
#   None
#######################################
function cleanup() {
    echo "coucou"
}

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
function get_dir() {
  echo "${SOMEDIR}"
}

#######################################
# Delete a file in a sophisticated manner.
# Arguments:
#   File to delete, a path.
# Returns:
#   0 if thing was deleted, non-zero on error.
#######################################
function del_thing() {
  rm "$1"
}

# TODO(mrmonkey): Handle the unlikely edge cases (bug ####)



#!/bin/bash
#
# Perform hot backups of Oracle databases.
# And so on ...


#######################################
# Cleanup files from the backup directory.
# Globals:
#   BACKUP_DIR
#   ORACLE_SID
# Arguments:
#   None
#######################################
function cleanup() {
    echo "coucou"
}

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
# Raise:
#   Error if directory does not exist.
#######################################
function get_dir() {
  echo "${SOMEDIR}"
}

#######################################
# Delete a file in a sophisticated manner.
# Arguments:
#   File to delete, a path.
# Returns:
#   0 if thing was deleted, non-zero on error.
#######################################
function del_thing() {
  rm "$1"
}

# TODO(mrmonkey): Handle the unlikely edge cases (bug ####)