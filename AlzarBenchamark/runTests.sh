echo "############### Python vs Cpp Code versions Test ###############"
start_all=`date +%s`
for i in configFile.txt configFile2.txt configFile3.txt configFile4.txt configFile5.txt configFile6.txt configFile7.txt configFile8.txt configFile9.txt configFile10.txt
do
  for j in *Set1 *Set2 *Set3 *Set4 *Set5 *Set6 *Set7 *Set8 *Set9 *Set10 *Set11
  do
    echo
    echo "############### Run for: $i"
    echo
    start=`date +%s`
    echo "[INFO] Cpp code test run....... "
    cd /home/useme/Przemek/CppVersion/ATS9870/DualPort/NPT_Average/ && make clean && make && ./ATS9870_NPT_Average $i $j
    echo
    echo "[INFO] Python code test run....... "
    echo
    #sleep 5
    python3 /home/useme/Przemek/PythonVersion/ATS9870/NPT_Average/ATS9870_NPT_Average.py $i $j
    end=`date +%s`
    runtime=$((end-start))
    echo "############### Test for $i finished in: $((runtime)) seconds"
    #sleep 5
  done
done
end_all=`date +%s`
runtime_all=$((end_all-start_all))
echo "############### Test for all sets finished in: $((runtime_all)) seconds"
