# coding: utf-8

import sublime
import sublime_plugin
from base64 import b64encode
from urllib import request
from re import search


class TheGodViewerCommand(sublime_plugin.EventListener):
	def on_hover(self, view, point, hover_zone):
		# if the mouse is on the code
		if hover_zone == sublime.HOVER_TEXT:
			region = view.find(".*", point)
			line = view.full_line(point)
			code = view.substr(sublime.Region(line.a, line.b))

			# img path
			path = search('<img[^>]*src="([^"]*)"', code)

			# if the mouse is on an image src
			if path:
				img = path.group(1)

				# if the img is hosted
				isHosted = search('(http|ftp)s?://', img)
				if isHosted:
					imgContent = request.urlopen(img)
					imgContent = str(b64encode(imgContent.read()), 'utf-8')
					popup = '<img src="data:image/png;base64,'+imgContent+'">'
					view.show_popup(popup, flags=sublime.HIDE_ON_MOUSE_MOVE_AWAY, location=point, max_width=500, max_height=500)
					return 

				# if the img is local
				cwd = sublime.active_window().folders()
				if not cwd:
					return

				imgPath = img.split('/')[-1]

				# check if this is not an img
				isImg = search('\.(png|PNG|jpg|JPG|JPEG|jpeg|svg|SVG)$', imgPath)
				if not isImg:
					return

				f = open(cwd[0] + '/' + imgPath, 'rb')
				if f:
					imgContent = str(b64encode(f.read()), 'utf-8')
					popup = '<img src="data:image/png;base64,'+imgContent+'">'
					view.show_popup(popup, flags=sublime.HIDE_ON_MOUSE_MOVE_AWAY, location=point, max_width=500, max_height=500)
					return 
















