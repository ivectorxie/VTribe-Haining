$procs = Get-CimInstance Win32_Process -Filter "Name='python.exe' OR Name='python3.13.exe'" | Where-Object { $_.CommandLine -like '*run_eva_full*' }
foreach ($x in $procs) { Stop-Process -Id $x.ProcessId -Force; Write-Host ("killed " + $x.ProcessId) }
Start-Sleep -Seconds 2
Start-Process -FilePath 'python' -ArgumentList 'run_eva_full.py','--workers','3' -WorkingDirectory 'S:\2 人事\4. 简历库\Processing\scripts' -WindowStyle Hidden -RedirectStandardOutput 'C:\Users\vecto\Documents\4.VTribe\eva_run_state\stdout.log' -RedirectStandardError 'C:\Users\vecto\Documents\4.VTribe\eva_run_state\stderr.log'
Write-Host 'relaunched v2'
