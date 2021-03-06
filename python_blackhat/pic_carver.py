import re
import zlib
import cv2

from scapy.all import *

pictures_directory  =  ""
faces_directory  =  ""
pcap_file  =  "bhp.pcap"

def http_assembler(pcap_file):

	carved_images  =  0
	faces_detected  =  0

	a  =  rdpcap(pcap_file)

	sessions  =  a.sessions()

	for session in sessions:

		http_payload  =  ""

		for packet  in session[session]:

			try:
				if packet[TCP].dport  ==  80 or packet[TCP].sport  ==  80:

					http_payload   +=  str(packet[TCP].payload)

			except:
				pass

		headers  =  get_http_headers(http_payload)

		if headers is None:
			continue

		image,image_type  =  extract_image(headers,http_payload)

		if image is not None and image_type is not None:
			
			file_name  =  "%s-pic_canver_%d.%s"% (pcap_file,carved_images,image_type)

			fd  =  open("%s/%s"% (pictures_directory,file_name),"wb")

			fd.write(image)
			fd.close()

			carved_images+=1

			try:
				result  =  faces_detected("%s/%s"% (pictures_directory,file_name),file_name)

				if result is True:
					faces_detected+=1
			except:
				pass

	return carved_images,faces_detected

carved_images,faces_detected   =   http_assembler(pcap_file)

print "Extracted: %d images" % carved_images
print "Detected: %d faces" % faces_detected