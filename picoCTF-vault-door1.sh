cat VaultDoor1.java | grep password.char | tr -d ' &&' | cut -f2 -d "(" | sort -g | cut -f2 -d "'" | tr -d "\n"
