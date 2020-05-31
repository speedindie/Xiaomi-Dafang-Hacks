#!/bin/sh

. /system/sdcard/www/cgi-bin/func.cgi
. /system/sdcard/scripts/common_functions.sh

export LD_LIBRARY_PATH=/system/lib
export LD_LIBRARY_PATH=/thirdlib:$LD_LIBRARY_PATH

echo "Content-type: text/html"
echo "Pragma: no-cache"
echo "Cache-Control: max-age=0, no-store, no-cache"
echo ""

if [ -n "$F_cmd" ]; then
  case "$F_cmd" in
  get_services)
	  echo "auto_night_mode#:#$(auto_night_mode status)#:#$(test -f /system/sdcard/config/autostart/auto-night-detection && echo 'true' || echo 'false')#:#false"
    echo "debug-on-osd#:#$(debug_on_osd status)#:#$(test -f /system/sdcard/config/autostart/debug-on-osd && echo 'true' || echo 'false')#:#false"
    echo "ftp_server#:#$(ftp_server status)#:#$(test -f /system/sdcard/config/autostart/ftp_server && echo 'true' || echo 'false')#:#false"
    echo "mqtt-control#:#$(mqtt_control status)#:#$(test -f /system/sdcard/config/autostart/mqtt-control && echo 'true' || echo 'false')#:#false"
    echo "mqtt-status#:#$(mqtt_status status)#:#$(test -f /system/sdcard/config/autostart/mqtt-status && echo 'true' || echo 'false')#:#false"
    echo "onvif-srvd#:#$(onvif_srvd status)#:#$(test -f /system/sdcard/config/autostart/onvif-srvd && echo 'true' || echo 'false')#:#false"
    echo "recording#:#$(recording status)#:#$(test -f /system/sdcard/config/autostart/recording && echo 'true' || echo 'false')#:#false"
    echo "rtsp-h264#:#$(rtsp_h264_server status)#:#$(test -f /system/sdcard/config/autostart/rtsp-h264 && echo 'true' || echo 'false')#:#false"
    echo "rtsp-mjpeg#:#$(rtsp_mjpeg_server status)#:#$(test -f /system/sdcard/config/autostart/rtsp-mjpeg && echo 'true' || echo 'false')#:#false"
	  echo "sound-on-startup#:#$(sound_on_startup status)#:#$(test -f /system/sdcard/config/autostart/sound-on-startup && echo 'true' || echo 'false')#:#false"
	  echo "telegram-bot#:#$(telegram_bot status)#:#$(test -f /system/sdcard/config/autostart/telegram-bot && echo 'true' || echo 'false')#:#false"
	  echo "timelapse#:#$(timelapse status)#:#$(test -f /system/sdcard/config/autostart/timelapse && echo 'true' || echo 'false')#:#false"
	return
	;;
  autoStartService)
    if [ $F_service == "auto_night_mode" ]; then
      F_service="auto-night-detection"
    fi
    if $F_action ; then
      echo "#!/bin/sh" > "/system/sdcard/config/autostart/${F_service}"
      echo "/system/sdcard/controlscripts/${F_service}" >> "/system/sdcard/config/autostart/${F_service}"
    else
      rm "/system/sdcard/config/autostart/${F_service}"
    fi
    return
    ;;
  services)
    $F_service $F_action
    return
    ;;
  getFiles)
    ip_addr=$(ip -o -4 addr show  | sed 's/.* inet \([^/]*\).*/\1/' | grep -v "127.0.0.1")
    for file in $(find /system/sdcard/DCIM/${F_dir}/ -type f)
      do                                                 
        if [[ -f $file ]]; then                           
          file_size=$(ls -lh $file | awk '{print $5}')                                          
          file_url=$(ls -lh $file | awk '{print $9}' | sed 's/\/system\/sdcard\/DCIM/\/viewer/')
          file_date=$(ls -lh $file | awk '{print $6 "-" $7 "-" $8}')                            
          file_name=$(ls -lh $file | awk '{print $9}' | awk -F / '{print $(NF)}')                                                                                                      
          echo "${file_name}#:#${file_size}#:#${file_date}#:#${file_url}"                                                                                    
        fi                                        
      done             
    return
    ;;

  del_config)
    F_file=$(echo ${F_file} | sed -e 's/%2F/\//g' | sed -e 's/viewer/system\/sdcard\/DCIM/') 
    echo "Remove ${F_file}"
    rm $F_file
  ;;
  restore_config)
    F_file=$(echo ${F_file} | sed -e 's/%2F/\//g' | sed -e 's/viewer/system\/sdcard\/DCIM/') 
    tar -xf $F_file -C /system/sdcard/config/
    echo "Restore done"
    /sbin/reboot
  ;;
  save_config)
    /system/sdcard/controlscripts/saveConfig.sh
  ;;
  reboot)
  	echo "Rebooting device..."
	  /sbin/reboot
	return
	;;
  shutdown)
	echo "Shutting down device.."
	/sbin/halt
	return
	;;
  *)
    echo "Unsupported command '$F_cmd'"
    ;;

  esac
  fi

exit 0

