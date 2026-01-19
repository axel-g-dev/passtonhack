### Ce que montre **le script**, factuellement

Dans la ligne clé :

```powershell
./Guide_Utilisateur_v03.pdf.exe -n MsMpEng.exe -k
```

* `MsMpEng.exe` = **processus du moteur antivirus**
* Ce processus appartient à **Microsoft Defender Antivirus**

### Correspondance correcte

| Élément             | Nom                  |
| ------------------- | -------------------- |
| Processus           | MsMpEng.exe          |
| Outil de sécurité   | **Windows Defender** |
| Nom attendu en flag | **windows_defender** |

### Flag final attendu

```
FLAG{windows_defender}
```


