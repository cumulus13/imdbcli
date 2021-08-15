#!c:/SDK/Anaconda3/python.exe
from __future__ import print_function
from safeprint import print as sprint
import imdb
import re
import argparse
from make_colors import make_colors
from pydebugger.debug import debug
import sys, os
import download
import clipboard
from unidecode import unidecode

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
			try:
				print(make_colors(str(x).upper(), 'b', 'y'), (32 - len(str(x))) * ' ', "=", unidecode(data.get(x)))
			except:
				try:
					print(make_colors(str(x).upper(), 'b', 'y'), (32 - len(str(x))) * ' ', "=", str(data.get(x)))
				except:
					try:
						sprint(make_colors(str(x).upper(), 'b', 'y'), (32 - len(str(x))) * ' ', "=", data.get(x))
					except:
						print(make_colors("error !"))

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
			# else:
			# 	download_poster_finish = True
			# 	download_thumb_finish = True
			# 	download_cover_is_finish = True
		if download_thumb_is_error:
			print(make_colors("No Image Thumb Url Found !", 'white', 'red', ['blink']))
		elif download_thumb_finish:
			print(make_colors("Successfull download thumb image !", 'white', 'red', ['blink']))
		if download_poster_is_error:
			print(make_colors("No Image Poster Url Found !", 'white', 'red', ['blink']))
		elif download_cover_is_finish:
			print(make_colors("Successfull download Poster image !", 'white', 'red', ['blink']))
				
		return data
		
	def cli(self, movie = None, id = None, download_cover = False, download_json = False, download_path = 'covers', cover_name = 'Poster', thumb_name = 'Thumb', clip = False):
		im = imdb.IMDb()
		if movie:
			data = im.search_movie(movie)
			n = 1
			for i in data:
				number = make_colors(str(n), 'cyan')
				if len(str(n)) == 1:
					number = make_colors("0" + str(n), 'cyan')
				
				title = make_colors(unidecode(i.get('long imdb title')), 'white', 'blue')
				ID = make_colors(i.getID(), 'red', 'white')
				print(number + ". " + title + "[" + ID + "]")
				n += 1
			try:
				q = input(make_colors("Select Number: ", 'b', 'y'))
			except:
				sys.exit()
			if q and str(q).strip().isdigit():
				idx = data[int(str(q).strip()) - 1].getID()
				# debug(idx = idx, debug = True)
				if clip:
					clipboard.copy("tt" + str(idx))
				elif int(q) <= len(data):
					self.details(idx, download_cover, download_json, download_path)
					clipboard.copy("tt" + str(idx))
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
		
		MOVIE_NAME = ''
		parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
		parser.add_argument('-m', '--movie', action = 'store', help = 'Search by Movie Name')
		parser.add_argument('-c', '--copy-id', action = 'store_true', help = 'Copy Id to Clipboard')
		parser.add_argument('-id', '--id', action = 'store', help = 'Search by Movie id, just number without "tt"')
		parser.add_argument('-d', '--download', action = 'store_true', help = 'Download data as json')
		parser.add_argument('-dc', '--download-cover', action = 'store_true', help = 'Download Image Poster and Thumb')
		parser.add_argument('-p', '--download-path', action = 'store', help = 'Save all of Download data to directory', default = 'covers')
		parser.add_argument('-cn', '--cover-name', action = 'store', help='Save Cover Poster as name, default: "Poster"', default = 'Poster')
		parser.add_argument('-tn', '--thumb-name', action = 'store', help='Save Thumb as name, default: "Thumb"', default = 'Thumb')
		if len(sys.argv) == 1:
			parser.print_help()
			sys.exit()
		elif len(sys.argv) > 1 and len([i for i in sys.argv[1:] if not i in parser._option_string_actions.keys()]) > 1:
			parser.add_argument('MOVIES', action = 'store', help = 'Search by Movie Name', nargs='*')
			MOVIE_NAME = True
		args = parser.parse_args()
		if MOVIE_NAME:
			movie = " ".join(args.MOVIES)
			debug(movie = movie)
			movie = re.split("\|", movie)
			debug(movie = movie)
		else:
			movie = args.movie
		if isinstance(movie, list):
			for i in movie:
				if i == 'c':
					i = clipboard.paste()
				self.cli(i, args.id, args.download_cover, args.download, args.download_path, args.cover_name, args.thumb_name, args.copy_id)
		else:
			if movie == 'c':
				movie = clipboard.paste()
			self.cli(movie, args.id, args.download_cover, args.download, args.download_path, args.cover_name, args.thumb_name, args.copy_id)
			
if __name__ == '__main__':
	c = imdbcli()
	c.usage()
		