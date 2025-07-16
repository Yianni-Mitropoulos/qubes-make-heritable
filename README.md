# make-heritable: Qubes TemplateVM File Heritability Helper

This tool lets you copy files or Firefox settings from a Qubes TemplateVM into `/etc/skel`, so that new AppVMs inherit them automatically.

## Clone the Repository
git clone https://github.com/Yianni-Mitropoulos/qubes-make-heritable.git
cd make-heritable

## Transfer to a TemplateVM with qvm-copy
# In the source VM (where you cloned the repo):
qvm-copy make-heritable.py

# In dom0, a prompt will ask you which VM to send it to.
# Select your target TemplateVM (e.g., debian-12-xfce).

## In the Target TemplateVM
# (Assume the file lands in ~/QubesIncoming/<source-vm>/make-heritable.py)

cd ~/QubesIncoming/<source-vm>
chmod +x make-heritable.py
sudo mv make-heritable.py /usr/local/bin/make-heritable

## Usage
# To make core Firefox settings heritable (about:config, user.js, default search engine, etc):
sudo make-heritable --firefox

# To make a specific file or directory heritable
sudo make-heritable <file-or-directory-relative-to-cwd>

## What Happens?
- The script places the file(s) into /etc/skel, so all newly created AppVMs from this TemplateVM inherit them in their home directory.
- With --firefox, it copies the essential Firefox user preferences but not your history, cookies, or extensions.

## Notes
- After copying, shut down the TemplateVM. After this, new AppVMs based on that template will inherit the configuration files that were made heritable.