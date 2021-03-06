#!/usr/bin/env python3

from modules.common.automation import *

class InstallerTemplate:

    _REPOS = [
        'T-S-A/smbspider',
        'byt3bl33d3r/CrackMapExec',
        'gojhonny/CredCrack',
        'jekyc/wig',
        'Dionach/CMSmap',
        'droope/droopescan',
        'ChrisTruncer/EyeWitness',
        'adaptivethreat/BloodHound',
        'lgandx/Responder',
        'ChrisTruncer/Just-Metadata',
        'ChrisTruncer/Egress-Assess',
        'Raikia/CredNinja',
        'Raikia/SMBCrunch',
        'Raikia/IPCheckScope',
        'Raikia/Misc-scripts',
        'secretsquirrel/SigThief',
        'enigma0x3/Misc-PowerShell-Stuff',
        '0x09AL/raven',
        'dafthack/MailSniper',
        'Arvanaghi/CheckPlease',
        'trustedsec/ptf',
        'Mr-Un1k0d3r/PowerLessShell',
        'Mr-Un1k0d3r/CatMyFish',
        'Mr-Un1k0d3r/MaliciousMacroGenerator',
        'Veil-Framework/Veil',
        'evilmog/ntlmv1-multi',
        'dirkjanm/PrivExchange',
        'rvrsh3ll/FindFrontableDomains',
        'trustedsec/egressbuster',
        'HarmJ0y/TrustVisualizer',
        'aboul3la/Sublist3r',
        'microsoft/ProcDump-for-Linux',
        'GreatSCT/GreatSCT',
        'AlessandroZ/LaZagne',
        'b-mueller/apkx',
	'wetw0rk/malicious-wordpress-plugin',
        'nccgroup/demiguise',
        'gnuradio/gnuradio',
        'johndekroon/serializekiller',
        'frohoff/ysoserial',
        'enjoiz/XXEinjector',
        'SpiderLabs/HostHunter',
        'smicallef/spiderfoot',
        'rofl0r/proxychains-ng',
        'scipag/vulscan',
        'rebootuser/LinEnum',
	'n00py/WPForce',
	'21y4d/nmapAutomator',
	'Tib3rius/AutoRecon',
	'LegendBegins/Overflow-Helper',
	'maurosoria/dirsearch',
	'linted/linuxprivchecker',
	'diego-treitos/linux-smart-enumeration',
	'PowerShellMafia/PowerSploit',
	'M4ximuss/Powerless',
	'epi052/recursive-gobuster',
	'TH3xACE/SUDO_KILLER',
	'hisxo/gitGraber',
	'chinarulezzz/pixload',
	'trustedsec/unicorn',
	'Anon-Exploiter/SUID3NUM',
	'samratashok/nishang',
	'kurobeats/fimap',
	'mzet-/linux-exploit-suggester',
	'jondonas/linux-exploit-suggester-2',
	'flozz/p0wny-shell',
	'Wphackedhelp/php-webshells', 
	'r3motecontrol/Ghostpack-CompiledBinaries', 
	'besimorhino/powercat', 
	'carlospolop/privilege-escalation-awesome-scripts-suite', 
	'sc0tfree/updog', 
	'bitsadmin/wesng',
	'3ndG4me/AutoBlue-MS17-010',
	'sensepost/ruler',
	'BC-SECURITY/Empire',
	'Sw4mpf0x/PowerLurk',
	'SecureAuthCorp/impacket',
	'cddmp/enum4linux-ng',
	'lijiejie/GitHack',
	'Flangvik/SharpCollection',    
    ]

    _ADDITIONAL_INSTRUCTIONS = {
        'Raikia/CredNinja': ['ln -s /opt/credninja-git/CredNinja.py /usr/local/bin/credninja'],
        'maurosoria/dirsearch': ['ln -s /opt/dirsearch-git/dirsearch.py /usr/local/bin/dirsearch'], 
        'ChrisTruncer/EyeWitness': ['cd ./Python/setup/; bash ./setup.sh'],
        'HarmJ0y/TrustVisualizer': ['pip3 install networkx'],
        'Tib3rius/AutoRecon': ['pip3 install -r /opt/autorecon-git/requirements.txt'],
        'Raikia/Misc-scripts': ['ln -s /opt/misc-scripts-git/np.py /usr/local/bin/np'],
        'chinarulezzz/pixload': ['apt -y -qq install libgd-perl libimage-exiftool-perl libstring-crc32-perl'],
        'rofl0r/proxychains-ng': [
            'cd /opt/proxychains-ng-git/; git pull -q', 
            'cd /opt/proxychains-ng-git/; make -s clean',
            'cd /opt/proxychains-ng-git/; ./configure --prefix=/usr --sysconfdir=/etc',
            'cd /opt/proxychains-ng-git/; make -s',
            'cd /opt/proxychains-ng-git/; make -s install',
            'ln -sf /usr/bin/proxychains4 /usr/local/bin/proxychains-ng'
        ],
        'scipag/vulscan': ['ln -s /opt/vulscan-git /usr/share/nmap/scripts/vulnscan'],
	'sensepost/ruler': ['ln -s /opt/ruler-git/bin/ruler /usr/local/bin/ruler']
    }

    def check(self, config):
        return True if command_exists("git") else "'git' package not installed"

    def install(self, config):
        print_status("Installing various github tools into /opt", 1)
        for proj in self._REPOS:
            print_status("Cloning {0}...".format(proj.split('/')[1]), 2)
            github_clone(proj, "/opt/")
            folder_name = "/opt/{0}-git".format(proj.split('/')[1].lower())
            run_command("cd {0}; git pull -q".format(folder_name))
            if proj in self._ADDITIONAL_INSTRUCTIONS:
                for instr in self._ADDITIONAL_INSTRUCTIONS[proj]:
                    run_command("cd {0}; {1}".format(folder_name, instr))
            print_success("Done!", 2)
        print_success("Done installing github tools!", 1)
        
        print_status("Writing GitHub update script", 1)
        update_file_contents = """#!/bin/bash
for d in /opt/* ; do
    echo "Starting $d"
    pushd $d &> /dev/null
    git fetch
    git pull origin master
    popd &> /dev/null
done
for d in /opt/cs_scripts/* ; do
    echo "Starting $d"
    pushd $d &> /dev/null
    git fetch
    git pull origin master
    popd &> /dev/null
done"""
        file_write('/opt/UpdateAll.sh', update_file_contents)
        run_command('chmod +x /opt/UpdateAll.sh')
        print_success('Done', 1)
