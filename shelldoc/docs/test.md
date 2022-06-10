## Description
Perform hot backups of Oracle databases.
And so on ...


**Interpreter** : `/bin/bash`

## `cleanup()`
**Description**
Cleanup files from the backup directory.


**Globals**
- BACKUP_DIR
- ORACLE_SID

**Arguments**
- None

## `get_dir()`
**Description**
Get configuration directory.


**Globals**
- SOMEDIR

**Arguments**
- None

**Outputs**
- Writes location to stdout

**See**
- [https://stackoverflow.com/questions/59895/getting-the-source-directory-of-a-bash-script-from-within](https://stackoverflow.com/questions/59895/getting-the-source-directory-of-a-bash-script-from-within)
- [del_thing](#del_thing)

## `del_thing()`
**Description**
Delete a file in a sophisticated manner.


**Arguments**
- File to delete, a path.

**Returns**
- 0 if thing was deleted, non-zero on error.

## `cleanup()`
**Description**
Cleanup files from the backup directory.


**Globals**
- BACKUP_DIR
- ORACLE_SID

**Arguments**
- None

## `get_dir()`
**Description**
Get configuration directory.


**Globals**
- SOMEDIR

**Arguments**
- None

**Outputs**
- Writes location to stdout

**See**
- [https://stackoverflow.com/questions/59895/getting-the-source-directory-of-a-bash-script-from-within](https://stackoverflow.com/questions/59895/getting-the-source-directory-of-a-bash-script-from-within)
- [del_thing](#del_thing)

**Raises**
- Error if directory does not exist.

## `del_thing()`
**Description**
Delete a file in a sophisticated manner.


**Arguments**
- File to delete, a path.

**Returns**
- 0 if thing was deleted, non-zero on error.

## Todos
- [ ] Handle the unlikely edge cases (bug ####)
