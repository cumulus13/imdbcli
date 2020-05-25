#!c:/SDK/Anaconda3/python.exe
import imdb
import argparse
from make_colors import make_colors
from pydebugger.debug import debug
import sys, os
import download

class imdbcli_error(Exception):
	pass

class imdbcli(object):
	def __init__(self):
		super(imdbcli, self)
		
	def details(self, id, download_cover = False, download_json = False, download_path = "covers", cover_name = 'Poster', thumb_name = 'Thumb'):
		im = imdb.IMDb()
		data = im.get_movie(id)
		download_cover_is_finish = False
		download_thumb_finish = False
		download_poster_finish = False
		download_poster_is_error = False
		download_thumb_is_error = False
		#print("Keys =", data.keys())
		for x in data.keys():
			print(make_colors(str(x).upper(), 'black', 'yellow'), (32 - len(str(x))) * ' ', "=", data.get(x))
			#print("Thumb  URL =", data.get('cover url'))
			#print("Poster URL =", data.get('full-size cover url'))
			if not download_cover_is_finish:
				if download_cover:
					if not os.path.isdir(download_path):
						os.makedirs(download_path)
					if not download_thumb_finish:
						if data.get('cover url'):
							download.download_img(data.get('cover url'), thumb_name, download_path, add_ext = True)
							download_thumb_finish = True
					else:
						download_thumb_is_error = True
					if not download_poster_finish:
						if data.get('full-size cover url'):
							download.download_img(data.get('full-size cover url'), cover_name, download_path, add_ext = True)
							download_poster_finish = True
						else:
							download_poster_is_error = True
				download_cover_is_finish = True
			else:
				download_poster_finish = True
				download_thumb_finish = True
				download_cover_is_finish = True
		if download_thumb_is_error:
			print(make_colors("No Image Thumb Url Found !", 'white', 'red', ['blink']))
		elif download_thumb_finish:
			print(make_colors("Successfull download thumb image !", 'white', 'red', ['blink']))
		if download_poster_is_error:
			print(make_colors("No Image Poster Url Found !", 'white', 'red', ['blink']))
		elif download_cover_is_finish:
			print(make_colors("Successfull download Poster image !", 'white', 'red', ['blink']))
				
		return data
		
	def cli(self, movie = None, id = None, download_cover = False, download_json = False, download_path = 'covers', cover_name = 'Poster', thumb_name = 'Thumb'):
		im = imdb.IMDb()
		if movie:
			data = im.search_movie(movie)
			n = 1
			for i in data:
				number = make_colors(str(n), 'cyan')
				if len(str(n)) == 1:
					number = make_colors("0" + str(n), 'cyan')
				
				title = make_colors(str(i.get('long imdb title')), 'white', 'blue')
				ID = make_colors(i.getID(), 'red', 'white')
				print(number + ". " + title + "[" + ID + "]")
				n += 1
			q = input(make_colors("Select Number: ", 'black', 'yellow'))
			if q and str(q).strip().isdigit():
				if int(q) <= len(data):
					self.details(data[int(str(q).strip()) - 1].getID(), download_cover, download_json, download_path)
				print(make_colors("Movie Selected:", 'black', 'yellow'), make_colors(data[int(str(q).strip()) - 1].get('long imdb title'), 'white', 'magenta'))
				
		elif id:
			data = im.get_movie(id)
			if data:
				self.details(id, download_cover, download_json, download_path)
				print(make_colors("Movie Selected:", 'black', 'yellow'), make_colors(data.get('long imdb title'), 'white', 'magenta'))
			else:
				print(make_colors("No Movie Found !", 'white', 'red', ['blink']))
		else:
			raise imdbcli_error(make_colors("No Movie or ID given !", 'white', 'red', ['blink']))
		
			
	def usage(self):
		parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
		parser.add_argument('-m', '--movie', action = 'store', help = 'Search by Movie Name')
		parser.add_argument('-id', '--id', action = 'store', help = 'Search by Movie id, just number without "tt"')
		parser.add_argument('-d', '--download', action = 'store_true', help = 'Download data as json')
		parser.add_argument('-c', '--download-cover', action = 'store_true', help = 'Download Image Poster and Thumb')
		parser.add_argument('-p', '--download-path', action = 'store', help = 'Save all of Download data to directory', default = 'covers')
		parser.add_argument('-cn', '--cover-name', action = 'store', help='Save Cover Poster as name, default: "Poster"', default = 'Poster')
		parser.add_argument('-tn', '--thumb-name', action = 'store', help='Save Thumb as name, default: "Thumb"', default = 'Thumb')
		if len(sys.argv) == 1:
			parser.print_help()
		else:
			args = parser.parse_args()
			self.cli(args.movie, args.id, args.download_cover, args.download, args.download_path, args.cover_name, args.thumb_name)
			
if __name__ == '__main__':
	c = imdbcli()
	c.usage()
		