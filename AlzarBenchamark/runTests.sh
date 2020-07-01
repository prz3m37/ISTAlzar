echo "############### Python vs Cpp Code versions Test ###############"
echo
start=$(date +"%s")
for i in {1..5}
  do
  echo "############### Test run number: $i  "
  for j in {1..3344}
    do
      echo
      echo "############### Test for configuration: Set$j"
      echo
      echo "[INFO] Cpp code test run....... "
      echo
      # shellcheck disable=SC2035
      cd /home/useme/Przemek/CppVersion/ATS9870/DualPort/NPT_Average/ && ./ATS9870_NPT_Average configurationFile.txt *Set$j
      echo
      echo "############### Test for $i finished in: $((runtime)) seconds"
  done
done
end=$(date +"%s")
runtime=$((end-start))
echo "############### Test for Cpp code finished in: $((runtime)) seconds ###############"

sleep 60

echo
start=$(date +"%s")
for i in {1..5}
  do
  echo "############### Test run number: $i  "
  for j in {1..3344}
    do
      echo
      echo "############### Test for configuration: Set$j"
      echo
      echo "[INFO] Python code test run....... "
      echo
      # shellcheck disable=SC2035
      python3 /home/useme/Przemek/PythonVersion/ATS9870/NPT_Average/ATS9870_NPT_Average.py configurationFile.txt *Set$j
      echo "############### Test for $i finished in: $((runtime)) seconds"
  done
done
end=$(date +"%s")
runtime=$((end-start))
echo "############### Test for Python code finished in: $((runtime)) seconds ###############"
