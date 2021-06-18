film <phrase>:
	filename = user.formatted_text(phrase, "kebab")
	user.switcher_focus("cmd")
	'ffmpeg -f dshow -i audio="Headset Microphone (Realtek High Definition Audio(SST))"  -f gdigrab -itsoffset 00:00:0.6 -i desktop -c:v libx264rgb -framerate 24 -crf 20 -preset ultrafast C:\\Users\\GamingAccount\\Desktop\\{filename}.mkv \n' 
	user.subtitles_transcript(filename)
	sleep(100ms)


stop recording: 
	user.switcher_focus("cmd")
	sleep(100ms)
	key(ctrl-c)
	user.close_sub_transcript() 
	original = user.get_subtitle_transcript_name()




create video: 
	user.switcher_focus("cmd")
	insert("(for /F %i in ('dir /B /A:-D /O:D *mkv') do @echo file '%i') > myvideos.txt")
	key(enter)
	sleep(500ms)
	insert("(for /F %i in ('dir /B /A:-D /O:D *srt') do @echo file '%i') > mysubtitles.txt")
	key(enter)
	sleep(500ms)
	insert("ffmpeg -y -f concat -safe 0 -i myvideos.txt -f concat -safe 0 -i mysubtitles.txt -map 0 -c:v copy -c:a copy -map 1 -c:s srt ConcatenatedVideoWithAudio.mkv")
	key(enter)
	sleep(1000ms)
	insert("ffmpeg -i ConcatenatedVideoWithAudio.mkv -c copy ConcatenatedVideoWithAudio.srt")
	
create advertising screen:
	user.switcher_focus("cmd")	 
	insert("ffmpeg -f lavfi -i color=size=2736X1824:duration=3:rate=29.97:color=black -vf "drawtext=font='Arial': text='ataraxy.consulting':x=(w-tw)/2:y=((h-text_h)/2)-(text_h-(th/4)): fontsize=250: fontcolor=white, drawtext=font='Arial': text='Hire Ataraxy To Document Your Projects!':x=(w-tw)/2:y=((h-text_h)/2)+(text_h-(th/4)): fontsize=100: fontcolor=white" test.mkv ")
	key(enter)

get trimming info: 
	user.switcher_focus("cmd")
	insert("cd originals \n")
	insert("get_movie_trimming_info.bat \n")


trim movies: 
	user.switcher_focus("cmd")
	insert("cd originals \n")
	insert("trim_stop_recording_command_from_movies.bat \n")


create front title:
	user.switcher_focus("cmd")	 
	title = "Simplest Custom Voice Commands"
	tagline = "Basic Command Words and Phrases"
	insert("ffmpeg -f lavfi -i color=size=2736X1824:duration=3:rate=29.97:color=black -vf \"drawtext=font='Arial': text='{title}':x=(w-tw)/2:y=((h-text_h)/2)-(text_h-(th/4)): fontsize=150: fontcolor=white, drawtext=font='Arial': text='{tagline}':x=(w-tw)/2:y=((h-text_h)/2)+(text_h-(th/4)): fontsize=100: fontcolor=white\" title.mkv \n")
	sleep(5000ms)
	insert("ffmpeg -f lavfi -i color=size=2736X1824:duration=3:rate=29.97:color=black -vf \"drawtext=font='Arial': text='{title}':x=(w-tw)/2:y=((h-text_h)/2)-(text_h-(th/4)): fontsize=150: fontcolor=white, drawtext=font='Arial': text='{tagline}':x=(w-tw)/2:y=((h-text_h)/2)+(text_h-(th/4)): fontsize=100: fontcolor=white\" -frames:v 1 thumbnail.png \n") 
	sleep (5000ms)
	insert("ffmpeg -f lavfi -i color=size=2736X1824:duration=3:rate=29.97:color=black -vf \"drawtext=font='Arial': text='ataraxy.consulting':x=(w-tw)/2:y=((h-text_h)/2)-(text_h-(th/4)): fontsize=250: fontcolor=white, drawtext=font='Arial': text='Hire Ataraxy To Document Your Projects!':x=(w-tw)/2:y=((h-text_h)/2)+(text_h-(th/4)): fontsize=100: fontcolor=white\" advertisement.mkv \n")
	sleep(5000ms)
	insert('ffmpeg -i "title.mkv" -f lavfi -i anullsrc=cl=stereo:r=44100 -shortest -y "title-sound.mkv" \n')
	sleep(5000ms)
	insert('ffmpeg -i "advertisement.mkv" -f lavfi -i anullsrc=cl=stereo:r=44100 -shortest -y "advertisement-sound.mkv" \n')
	sleep(5000ms)

create front subtitles:
	user.switcher_focus("cmd")	 
	title = "Simplest Custom Voice Commands"
	tagline = "Basic Command Words and Phrases"
	insert('echo 1 > title.srt \n')
	insert('echo 00:00:00,000 --^> 00:00:03,000 >> title.srt \n') 
	insert('echo {title} >> title.srt \n')
	insert('echo {tagline} >> title.srt \n')
	insert('echo 1 > advertisement.srt \n')
	insert('echo 00:00:00,000 --^> 00:00:03,000 >> advertisement.srt \n') 
	insert('echo ataraxy.consulting >> advertisement.srt \n')
	insert('echo Hire Ataraxy To Document Your Projects >> advertisement.srt \n')

create final movie:
	user.switcher_focus("cmd")	 
	insert("echo file 'title-sound.mkv' > final_videos.txt \n")
	insert("echo file 'advertisement-sound.mkv' >> final_videos.txt \n")
	insert("echo file 'title.srt' > final_subtitles.txt \n")
	insert("echo file 'advertisement.srt' >> final_subtitles.txt \n")
	insert("(for /F %i in ('dir /B /A:-D /O:D *trim.mkv') do @echo file '%i') >> final_videos.txt \n" )
	sleep(300ms)
	insert("(for /F %i in ('dir /B /A:-D /O:D *trim.srt') do @echo file '%i') >> final_subtitles.txt \n")
	sleep(300ms)
	insert("ffmpeg -y -f concat -safe 0 -i final_videos.txt -f concat -safe 0 -i final_subtitles.txt -map 0 -c:v copy -c:a copy -map 1 -c:s srt final_video.mkv \n")


get final subtitles: 
	user.switcher_focus("cmd")
	insert("ffmpeg -i final_video.mkv -c copy final_video.srt")















