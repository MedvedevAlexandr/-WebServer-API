let submit=document.getElementById('btn')
let save=document.getElementById('save')

let date = document.getElementById('date');
let klass = document.getElementById('klass');

let request = {
  klass: null,
  date: null
}

let test = {
    "2021-04-16": []
  }

submit.addEventListener('click', (Event) => {
	Event.preventDefault();

	//нажатие на кнопку...
	request.date = date.value;
	request.klass = klass.value;

	fetch('edit-schedule', {
	  headers: {
	    'Content-Type': 'application/json'
	  },

	  method: 'POST',
	  body: JSON.stringify(request),
	})
	  .then((data) => {
	    return data.json();
	  })

	  .then((data) => {
	    console.log(data[date.value]);
	    // data[date.value]
	    // data['2021-06-15']
	    if (Object.keys(data).length != 0) {
		    // console.log('пуст');
	    data[date.value].map((item, index) => (
		  document.getElementById('tab').innerHTML += `<tr><td style="width: 38px;">&nbsp; ${++index}</td><td style="width: 151px;"><input id="lasson" onchange="check(this.value, this.getAttribute('alias'))" value="${item.lesson}" type="text" class="edittable" alias="${item.lesson}"></td><td style="width: 390px;"><input id="homework" onchange="check(this.value, this.getAttribute('alias'))" value="${item.homework}" type="text" class="edittable" alias="${item.homework}"></td></tr>`
		));
		} else {
			// дописать
		}
	  });
});

function check(current, alias) {
    if (current !== alias) {
      save.removeAttribute('disabled');
    } else {
      save.setAttribute('disabled', true);
    }
  }

// save.addEventListener('click', (Event) => {
// 	Event.preventDefault();
// }
