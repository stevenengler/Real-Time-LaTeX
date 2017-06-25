#!/usr/bin/env bash
#
tl_download_directory="$HOME/texlive_download"
tl_installer_url="http://mirror.ctan.org/systems/texlive/tlnet/install-tl-unx.tar.gz"
# if this path breaks, please get the correct URL from here:
#       https://www.tug.org/texlive/acquire-netinstall.html
#
echo "The script will update the APT package list, install python3-watchdog, download the TeX Live"\
     "installation scripts to \"$tl_download_directory\", install TeX Live, and install latexmk with tlmgr."
#
echo ""
echo "Do you want to continue?"
select yn in "Yes" "No"; do
    case $yn in
        Yes ) break;;
        No ) exit;;
    esac
done
echo ""
#
if [ -d "$tl_download_directory" ]; then
  echo "The \"$tl_download_directory\" directory already exists. Please delete it and run this script again."
  exit
fi
#
echo "Downloading and unpacking the TeX Live (online) installer."
echo ""
#
mkdir "$tl_download_directory" && cd "$_"
wget "$tl_installer_url" || exit 1
tar -xf install-tl-unx.tar.gz
cd install-tl-*
#
echo ""
echo "The TeX Live download/installation menu is about to begin. You can configure your TeX Live installation"\
     "however you wish, but I recommend disabling the options for the documentation and source installation"\
     "('macro/font doc tree' and 'macro/font source tree') as they take up a lot of space. You can also disable"\
     "the installation of extra languages to save space. The download will take anywhere from 30 minutes to"\
     "several hours depending on your internet speed and the packages that you select."
echo ""
#
read -p "Press enter to continue..."
#
sudo ./install-tl
#
echo ""
echo "If everything installed correctly, the output of the installer above should list three paths for TeX Live:"\
     "the PATH, MANPATH, and INFOPATH. Please enter them below."
echo ""
#
read -p "Enter the TeX Live PATH: " tl_path
read -p "Enter the TeX Live MANPATH: " tl_manpath
read -p "Enter the TeX Live INFOPATH: " tl_infopath
#
printf "\n" >> ~/.bashrc
printf "export PATH=\"$tl_path:\$PATH\"\n" >> ~/.bashrc
printf "export MANPATH=\"$tl_manpath:\$MANPATH\"\n" >> ~/.bashrc
printf "export INFOPATH=\"$tl_infopath:\$INFOPATH\"\n" >> ~/.bashrc
#
echo ""
echo "The three lines below have been appended to your '~/.bashrc' file."
echo ""
#
printf "export PATH=\"$tl_path:\$PATH\"\n"
printf "export MANPATH=\"$tl_manpath:\$MANPATH\"\n"
printf "export INFOPATH=\"$tl_infopath:\$INFOPATH\"\n"
#
echo ""
echo "Installing latexmk with tlmgr if it has not already been installed."
echo ""
#
sudo env PATH="$PATH" tlmgr install latexmk
#
echo ""
echo "The installation has completed. You can delete the \"$tl_download_directory\" directory if you wish."
echo ""
#
