$ip = Read-Host -Prompt "Enter IP Range" 
for($ipe=1; $ipe -le 254; $ipe++) {$($(ping -n 1 $ip$ipe | Select-String "bytes=32") -Split(" ") -Split(":")) | Select-String "$ip"}