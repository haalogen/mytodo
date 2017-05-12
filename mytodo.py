import sqlite3
from bottle import route, run, template, request
from bottle import debug, static_file, redirect
from enum import Enum

PATH_TO_STATIC_FILES = './static/'

DB_NAME = 'mytodo.db'

class Status(Enum):
	"""docstring for Status"""
	UNDONE = 0
	DONE = 1



class Priority(Enum):
	"""docstring for Priority"""
	HIGH = 1
	NORMAL = 2
	LOW = 3



# Create An SQL Database
con = sqlite3.connect(DB_NAME)
con.execute("""CREATE TABLE IF NOT EXISTS todo (
	id INTEGER PRIMARY KEY,
	description TEXT(100) NOT NULL, -- task description

	/* HIGH = 1, NORMAL = 2, LOW = 3 */
	priority INTEGER NOT NULL,

	/* Date of task deadline, Example: 23.05(fr)  */
	deadline TEXT(10),

	/* 0 -- undone task, 1 -- completed task */
	status BOOL NOT NULL
)""")



# Gives static files
@route('/static/<filename:path>')
def server_static(filename):
	return static_file(filename, root=PATH_TO_STATIC_FILES)


# Shows current todo-list
@route('/')
def todo_list():
	# Connect to DB and select all undone tasks
	_conn = sqlite3.connect(DB_NAME)
	c = _conn.cursor()
	c.execute("""SELECT priority, deadline, description, id FROM todo
		WHERE status LIKE '{status}'
		""".format(status=Status.UNDONE.value))

	# 'result' looks like this:
	# [1, '12.05(пт)', ('Купить сахар'), 13 ...]
	result = c.fetchall()
	c.close()

	print(result)
	# return tasks list as a table made from template
	return template('current.tpl', rows=result)



# Edits existing task
@route('/edit/<no:int>', method='GET')
def edit_item(no):
	if request.GET.update: # we got edited data
		edit = request.GET.description.strip() # edited descr
		priority = request.GET.priority.strip()
		deadline = request.GET.deadline.strip()

		# update task data in DB
		conn = sqlite3.connect(DB_NAME)
		c = conn.cursor()
		c.execute("""UPDATE todo SET description = ?, priority = ?,
			deadline = ? WHERE id LIKE ?""",
							(edit, priority, deadline, no))
		conn.commit()

		redirect('/')


# Adds new task
@route('/new', method='GET')
def new_item():
	description = request.GET.description.strip() # new descr
	priority = request.GET.priority.strip()
	deadline = request.GET.deadline.strip()

	# Connect to DB and add a new undone task
	conn = sqlite3.connect(DB_NAME)
	c = conn.cursor()

	c.execute("""INSERT INTO todo
	(description, priority, deadline, status) VALUES
	(?,?,?,?)
	""",
	(description, priority, deadline, Status.UNDONE.value))

	conn.commit()
	c.close()

	redirect('/')



# Completes existing task
@route('/complete/<no:int>', method='GET')
def complete_item(no):
	# remove task from DB
	conn = sqlite3.connect(DB_NAME)
	c = conn.cursor()
	c.execute("DELETE FROM todo WHERE id=?", (no,))
	conn.commit()

	redirect('/')


debug(True) # shows a full stacktrace of the Python interpreter
# 'reloader' watches for web-server script change
run(port=8081, reloader=True)