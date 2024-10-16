# File log untuk menyimpan input
LOGFILE="/data/data/com.termux/files/usr/var/sysinfo/logketikan.txt"

# Membuat direktori jika belum ada
mkdir -p /data/data/com.termux/files/usr/var/sysinfo

# Fungsi untuk mencatat input dengan format yang diinginkan
log_input() {
    current_time=$(date +"%H:%M:%S") # Format jam
    current_date=$(date +"%Y-%m-%d") # Format tanggal
    echo "$1 : [$current_time] [$current_date]" >> "$LOGFILE"
}

# Menyimpan input yang dimasukkan ke dalam log
PROMPT_COMMAND='log_input "$(history 1 | sed "s/^[ ]*[0-9]\+[ ]*//")"'
