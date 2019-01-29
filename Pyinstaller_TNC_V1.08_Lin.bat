pyinstaller -F --clean --distpath=Distribution_TNC_V12_S1P08  TNC_V1.08.spec 

echo ===========================================
echo Copying Documents to Distribution Directory
echo ===========================================
mkdir ./Distribution_TNC_V12_S1P08/Documents/
cp -r ./Documents ./Distribution_TNC_V12_S1P08/
echo =====================
echo ***Done Processing***
echo =====================

