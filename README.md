[Home Page](http://betinho89.com/sublime-sourcegear-vault/)

# Source Gear - Vault for Sublime text

## About

This is a Sublime Text plugin that allows to have an interface between Vault and Sublime.

![Screenshot](http://betinho89.com/sublime-sourcegear-vault/plugin_sublime_vault.png)

The plugin allows you to perform five frequently used Vault operations.
1. `Get Latest version`. Retrieve the latest version of files or folders in the repository.
2. `Check out`. Checkout files from the repository.
3. `Check in`. Commit the items in the pending changeset list specified by repositorypath(s).
4. `Undo Check out`. Undo a checkout, reverting changes back to the data in the repository.
5. `Properties`. Display the properties of the latest version from a file or folder.

## Installation

First of all, be sure you have [Vault Client](https://sourcegear.com/vault/downloads.html).

With [Package Control](http://wbond.net/sublime_packages/package_control):

1. Run “Package Control: Add Repository” command, paste the github URL `https://github.com/betinho89/sublime-sourcegear-vault/`.
2. Run “Package Control: Install Package” command, then find and install `sublime-sourcegear-vault plugin`.
2. Restart ST editor (if required)

Manually:

1. Clone or [download](https://github.com/betinho89/sublime-sourcegear-vault/archive/master.zip) git repo into your packages folder (in ST, find Browse Packages... menu item to open this folder)
2. Restart ST editor (if required)

## Options

```javascript
{
  // Server and authentication information
  "host": "",                 // Hostname of the server to connect to.
  "ssl": false,               // Enables SSL for server connection.
  "username": "",             // Username to use when connecting to server.
  "password": "",             // Password to use when connecting to server.
  "repositoryname": "",       // Repository to connect to.

  "vault_path": "",           // Replace with your own path to vault.exe
  "show_success": true        // Enables or disables a message to be displayed after each operation
}
```

## Key Binds

| Windows | Command |
|---------|---------|
|<kbd>Ctrl</kbd><kbd>Alt</kbd><kbd>G</kbd>|`Get Latest version`
|<kbd>Ctrl</kbd><kbd>Alt</kbd><kbd>O</kbd>|`Check out`
|<kbd>Ctrl</kbd><kbd>Alt</kbd><kbd>I</kbd>|`Check in`
|<kbd>Ctrl</kbd><kbd>Alt</kbd><kbd>Z</kbd>|`Undo Check out`
|<kbd>Ctrl</kbd><kbd>Alt</kbd><kbd>L</kbd>|`Properties`

## Usage

 - **Open Vault at File** via the editor context menu.
![Screenshot](http://betinho89.com/sublime-sourcegear-vault/plugin_sublime_vault_context_file.jpg)
 - **Open Vault at Project Folder** via the sidebar context menu.
![Screenshot](http://betinho89.com/sublime-sourcegear-vault/plugin_sublime_vault_context_sidebar.jpg)

## Common problems

1. Vault path not found, in Windows the path need have double slashe `\\`.
2. Add "vault.exe" to the list of allowed applications in your antivirus.

## License

Licensed under the MIT license.

## Donations

If you like this plugin and want to show your appreciation, you can buy me a coffee.

[![PayPal](https://www.paypalobjects.com/es_XC/MX/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=5BMAPEVBX9SJJ)
