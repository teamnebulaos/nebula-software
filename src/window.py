import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, GLib, Gio, GdkPixbuf
import json
import requests
import os
import subprocess

@Gtk.Template(resource_path='/org/nebula/Software/window.ui')
class NebulaSoftwareWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'NebulaSoftwareWindow'

    banner_image = Gtk.Template.Child()
    changelog_label = Gtk.Template.Child()
    refresh_button = Gtk.Template.Child()
    install_button = Gtk.Template.Child()
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_version = "1.0.0"
        self.setup_signals()
        self.check_updates()

    def setup_signals(self):
        self.refresh_button.connect('clicked', self.on_refresh_clicked)
        self.install_button.connect('clicked', self.on_install_clicked)

    def check_updates(self):
        try:
            # Check for updates from GitHub
            api_url = "https://api.github.com/repos/teamnebulaos/repo/releases/latest"
            response = requests.get(api_url)
            release_data = response.json()
            
            latest_version = release_data['tag_name']
            if latest_version > self.current_version:
                # Download and parse update manifest
                manifest_url = f"https://raw.githubusercontent.com/teamnebulaos/repo/{latest_version}/update_manifest.json"
                manifest_response = requests.get(manifest_url)
                if manifest_response.status_code == 200:
                    self.update_manifest = manifest_response.json()
                    
                # Download and show banner
                banner_url = f"https://raw.githubusercontent.com/teamnebulaos/repo/{latest_version}/banner.png"
                banner_response = requests.get(banner_url)
                if banner_response.status_code == 200:
                    with open('/tmp/update_banner.png', 'wb') as f:
                        f.write(banner_response.content)
                    pixbuf = GdkPixbuf.Pixbuf.new_from_file('/tmp/update_banner.png')
                    self.banner_image.set_from_pixbuf(pixbuf)

                # Download and show changelog
                changelog_url = f"https://raw.githubusercontent.com/teamnebulaos/repo/{latest_version}/changelog.txt"
                changelog_response = requests.get(changelog_url)
                if changelog_response.status_code == 200:
                    update_type = self.update_manifest.get('release_type', 'update')
                    changelog_text = f"New {update_type} available!\n\n"
                    changelog_text += changelog_response.text
                    self.changelog_label.set_text(changelog_text)
                
                self.install_button.set_sensitive(True)
            else:
                self.changelog_label.set_text("System is up to date")
                self.install_button.set_sensitive(False)

        except Exception as e:
            self.changelog_label.set_text(f"Error checking for updates: {str(e)}")
            self.install_button.set_sensitive(False)

    def on_refresh_clicked(self, button):
        self.check_updates()

    def on_install_clicked(self, button):
        try:
            if not hasattr(self, 'update_manifest'):
                raise Exception("No update manifest available")

            # Process package updates
            for package in self.update_manifest.get('package_updates', []):
                if package['action'] == 'install' or package['action'] == 'update':
                    subprocess.run(['sudo', 'pacman', '-S', '--noconfirm', f"{package['name']}"])
                elif package['action'] == 'remove':
                    subprocess.run(['sudo', 'pacman', '-R', '--noconfirm', f"{package['name']}"])

            # Download and install update files
            for file in self.update_manifest.get('update_files', []):
                file_url = f"https://raw.githubusercontent.com/teamnebulaos/repo/{self.update_manifest['version']}/files{file['path']}"
                response = requests.get(file_url)
                if response.status_code == 200:
                    # Verify checksum
                    if self.verify_checksum(response.content, file['checksum']):
                        # Create directory if it doesn't exist
                        os.makedirs(os.path.dirname(file['path']), exist_ok=True)
                        # Install file
                        with open(file['path'], 'wb') as f:
                            f.write(response.content)
                        # Set executable permission for binaries
                        if file['type'] == 'binary':
                            os.chmod(file['path'], 0o755)

            # Execute system commands
            for command in self.update_manifest.get('system_commands', []):
                subprocess.run(['sudo', 'sh', '-c', command])

            self.changelog_label.set_text("Update completed successfully!")
            self.install_button.set_sensitive(False)
            
            # Update current version
            self.current_version = self.update_manifest['version']
            
        except Exception as e:
            self.changelog_label.set_text(f"Error during update: {str(e)}")

    def verify_checksum(self, content, expected_checksum):
        import hashlib
        algorithm, hash_value = expected_checksum.split(':')
        if algorithm == 'sha256':
            actual_hash = hashlib.sha256(content).hexdigest()
            return actual_hash == hash_value
        return False
