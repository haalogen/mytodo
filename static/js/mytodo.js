function httpGetAsync(theUrl) {
	var xmlHttp = new XMLHttpRequest();

	xmlHttp.open("GET", theUrl, true); // true for asynchronous
	xmlHttp.send(null);
}


function showTaskEditForm (id) {
	const taskEditSection = document.querySelector(`#task-${id} .task-edit`);
	taskEditSection.classList.toggle('hidden');
}

function showNewTaskForm () {
	const taskNewSection = document.querySelector('#task-new');
	taskNewSection.classList.toggle('hidden');
}

function editTask (id) {
	console.log(id);
}


function completeTask (id) {
	const taskToComplete = document.querySelector(`#task-${id}`);
	const description = taskToComplete.querySelector(".task-description")
		.innerHTML;
	const deadline = taskToComplete.querySelector(".task-deadline")
		.innerHTML;
	const ans = confirm(`Вы действительно хотите удалить задачу \n
		"${deadline}, ${description}"?`);

	if (ans) { // Answer is 'OK'
		// delete task
		console.log(taskToComplete, 'will be deleted');
		httpGetAsync(`/complete/${id}`);
		location.reload(); // reload page
	} else { // Answer is 'Cancel'
		console.log(taskToComplete, "won't be deleted");
	};

}

