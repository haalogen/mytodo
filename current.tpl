%# Template of Current ToDo-list

% rebase('base.tpl', title='Current ToDo')

<p>Текущие задачи:</p>



<div class="tasks">

<button onclick="showNewTaskForm()">Добавить задачу</button>
<!-- New task adding form -->
<div id="task-new" class="task hidden">
	<div class="task-edit">
		<form action="/new" method="GET">
			<input type="number" min="1" max="3"
				value="2" name="priority">
			<input type="text" value="01.01(пн)"
				name="deadline">
			<textarea cols=50 name="description"></textarea>
			<button type="submit" name="add" >Добавить</button>
		</form>
	</div><!-- /task-edit -->
</div><!-- /task -->

<!-- Current tasks -->
%for row in rows:
	%priority = row[0]
	%deadline = row[1]
	%description = row[2]
	%id = row[3]
	<div id="task-{{id}}" class="task">
		<div class="task-priority priority-{{priority}}"></div>
		<div class="task-deadline">{{deadline}}</div>
		<div class="task-description">{{description}}</div>
		<div class="task-buttons">
			<button onclick="showTaskEditForm({{id}})">Изменить</button>
			<button onclick="completeTask({{id}})">Завершить</button>
		</div>

	<div class="task-edit hidden">
		<form action="/edit/{{id}}" method="GET">
			<input type="number" min="1" max="3"
				value="{{priority}}" name="priority">
			<input type="text" value="{{deadline}}"
				name="deadline">
			<textarea cols=50 name="description">{{description}}</textarea>
			<button type="submit" onclick="editTask({{id}})" name="update" >Обновить</button>
		</form>
	</div><!-- /task-edit -->
	</div><!-- /task -->
%end
</div><!-- /tasks -->

<script src="static/js/mytodo.js"></script>