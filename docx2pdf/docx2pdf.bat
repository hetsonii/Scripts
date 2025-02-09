:: Convert all DOCX files in the current directory to PDF

@echo off
setlocal enabledelayedexpansion

:: Create a temporary VBA script
echo Set objWord = CreateObject("Word.Application") > convert.vbs
echo objWord.Visible = False >> convert.vbs
echo Set objFSO = CreateObject("Scripting.FileSystemObject") >> convert.vbs
echo Set objFolder = objFSO.GetFolder(".") >> convert.vbs
echo For Each objFile In objFolder.Files >> convert.vbs
echo     If LCase(objFSO.GetExtensionName(objFile.Name)) = "docx" Then >> convert.vbs
echo         Set objDoc = objWord.Documents.Open(objFile.Path) >> convert.vbs
echo         pdfPath = objFSO.GetParentFolderName(objFile.Path) ^& "\" ^& objFSO.GetBaseName(objFile.Path) ^& ".pdf" >> convert.vbs
echo         objDoc.SaveAs2 pdfPath, 17 >> convert.vbs
echo         objDoc.Close False >> convert.vbs
echo     End If >> convert.vbs
echo Next >> convert.vbs
echo objWord.Quit >> convert.vbs

:: Run the script
cscript //nologo convert.vbs

:: Cleanup
del convert.vbs

echo Conversion completed!
pause
