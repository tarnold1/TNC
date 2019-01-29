pyinstaller -F --clean --distpath=Distribution_TNC_V11_S1P07  TNC_V1.07.spec 

echo ===========================================
echo Copying Documents to Distribution Directory
echo ===========================================
mkdir ./Distribution_TNC_V11_S1P07/Documents/
cp -r ./Documents ./Distribution_TNC_V11_S1P07/
echo =====================
echo ***Done Processing***
echo =====================

