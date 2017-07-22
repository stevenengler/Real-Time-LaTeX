#!/usr/bin/env python3
#
import subprocess
import os
import time
import traceback
import gzip
import shutil
#
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
#
class ChangeHandler(PatternMatchingEventHandler):
	# Only watch for changes to .tex files
	patterns = ["*.tex"]
	#
	def process(self, event):
		"""
		event.event_type
			'modified' | 'created' | 'moved' | 'deleted'
		event.is_directory
			True | False
		event.src_path
			path/to/observed/file
		"""
		#
		if event.is_directory:
			return
		#
		try:
			latex_project_filename = 'latex_project.config'
			compiled_path_relative_to_project_path = "compiled"
			#
			# First, move up the directory tree to find the project file
			modified_file = event.src_path
			modified_dir = os.path.dirname(modified_file)
			project_directory = self.get_project_directory(modified_dir, latex_project_filename)
			if project_directory is None:
				print('Python script: Project file not found.')
				return
			#
			# Using the project file, find the source file to be compiled
			src_files = self.get_source_files(project_directory, latex_project_filename)
			if src_files is None or len(src_files) == 0:
				print('Python script: Source files not found.')
				return
			#
			for src_file in src_files:
				print('Python script: Starting file \''+src_file+'\'')
				# Now the tex file can be compiled
				src_file_relative_to_project_path = os.path.relpath(src_file, project_directory)
				filename = os.path.splitext(os.path.basename(src_file))[0]
				#
				# Reasoning for commands is listed below:
				#    -recorder-		: Since Tex Live changed the filename structure of the texlive#.lsf(?), Latexmk cannot use these files properly and gives an error. Hopefully latexmk will fix this in the future
				#    -synctex=-1	: We need to edit the synctex later, so don't compress it
				#    -interaction=nonstopmode	: We don't want the script to prompt for input when errors occur
				#    -file-line-error	: Gives more detailed error messages
				commands = []
				commands.append("cd \""+project_directory+"\"")
				commands.append(" && mkdir -p \""+compiled_path_relative_to_project_path+"\"")
				commands.append(" && latexmk -pdf -recorder- -outdir=\""+compiled_path_relative_to_project_path+"\" -aux-directory=\""+compiled_path_relative_to_project_path+"\" -pdflatex='pdflatex -synctex=-1 -interaction=nonstopmode -file-line-error' \""+src_file_relative_to_project_path+"\"")
				commands.append(" | grep -A 5 '.*:[0-9]*:.*\\|!.*'")
				commands.append(" > \""+compiled_path_relative_to_project_path+'/'+filename+".err\"")
				#
				print(''.join(commands))
				subprocess.call(''.join(commands), shell=True)
				#
				# Finally, the synctex has to be modified to use relative paths instead of absolute paths
				self.fix_synctex(project_directory, compiled_path_relative_to_project_path, filename)
			#
			print('Python script: Finished latexmk...')
		except:
			traceback.print_exc()
		#
	#
	def on_modified(self, event):
		self.process(event)
	#
	def on_created(self, event):
		self.process(event)
	#
	def on_moved(self, event):
		self.process(event)
	#
	def get_project_directory(self, startDir, projectFilename):
		project_directory = startDir
		#
		while os.path.isdir(project_directory) and not os.path.isfile(project_directory+'/'+projectFilename):
			project_directory = os.path.dirname(project_directory)
		#
		if project_directory == '':
			# didn't find the project file
			project_directory = None
		#
		return project_directory
	#
	def get_source_files(self, projectDirectory, projectFilename):
		files_to_compile = []
		with open(projectDirectory+'/'+projectFilename, 'r') as f:
			for line in f:
				line = line.strip()
				if len(line) > 0 and line[0] != '#':
					# if first non-whitespace character is not a '#' and line is not empty
					files_to_compile.append(line)
				#
			#
		#
		for x in range(len(files_to_compile)):
			if not os.path.isfile(projectDirectory+'/'+files_to_compile[x]):
				print('Python script: Not a file ('+projectDirectory+'/'+files_to_compile[x]+')')
				files_to_compile[x] = None
			#
		#
		src_files = [projectDirectory+'/'+f for f in files_to_compile if f is not None]
		return src_files
	#
	def fix_synctex(self, project_directory, compiled_path_relative_to_project_path, filename):
		old_synctex = project_directory+'/'+compiled_path_relative_to_project_path+'/'+filename+'.synctex'
		new_synctex = project_directory+'/'+compiled_path_relative_to_project_path+'/'+filename+'.synctex.new'
		#
		if os.path.isfile(old_synctex):
			f1 = open(old_synctex, 'r')
			f2 = open(new_synctex, 'w')
			#
			project_path_relative_to_compiled_path = os.path.relpath(project_directory, project_directory+'/'+compiled_path_relative_to_project_path)
			for line in f1:
				f2.write(line.replace(os.path.abspath(project_directory), project_path_relative_to_compiled_path))
			#
			f1.close()
			f2.close()
			os.remove(old_synctex)
			#os.rename(new_synctex, old_synctex)
			#
			with open(new_synctex, 'rb') as f_in, gzip.open(old_synctex+'.gz', 'wb') as f_out:
				shutil.copyfileobj(f_in, f_out)
			#
			os.remove(new_synctex)
		#
	#
#
if __name__ == '__main__':
	handler = ChangeHandler()
	directory = './'
	observer = Observer()
	#
	if not os.path.exists(directory):
		os.makedirs(directory)
	#
	observer.schedule(handler, directory, recursive=True)
	observer.start()
	#
	try:
		while True:
			time.sleep(60*5)
			# Sleep for 5 minutes (amount doesn't really matter)
		#
	except KeyboardInterrupt:
		observer.stop()
	#
	observer.join()
	print('')
	# Add an extra new line
#
