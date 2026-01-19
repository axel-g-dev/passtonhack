En analysant statiquement le script PowerShell :

* Les chaînes Base64 décodées montrent un **Rename-Item** depuis
  `\Backstab64.exe`
  vers
  `Guide_Utilisateur_v03.pdf.exe`.
* Le binaire ensuite exécuté en boucle (`Guide_Utilisateur_v03.pdf.exe`) est donc **un renommage** destiné à masquer le véritable malware.

**Le nom initial de l’exécutable malveillant est :**

**FLAG{backstab64.exe}**
