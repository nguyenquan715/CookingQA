$("#question").keypress((event)=>{			
	if(event.keyCode=='13'){
		let question = $("#question")[0].value;
		//Reset question & answer
		$("#answer")[0].innerHTML = "";
		// $("#question")[0].value = "";								
		if(question == ""){
			$("#answer")[0].innerText = "You must enter your question!";
			return;
		}
		$.ajax({
			method:"POST",
			url:"/question",
			contentType:"application/json;charset=utf-8",
			data: JSON.stringify({"question": question})
		}).done((data)=>{
			console.log(data);
			if(typeof data == "string"){
				$("#answer")[0].innerHTML = `<h2>${data}</h2>`;
				return;
			}
			let ques_class = data["class"];
			let ing_entities = data["ing_entities"];
			let answer = data["answer"];
			if(typeof answer == "string"){
				$("#answer")[0].innerHTML = `<h2>${answer}</h2>`;
				return;
			}
			for(let i=0; i<answer.length; i++){
				if(!answer[i]["hits"]){
					$("#answer")[0].innerHTML = `<h2>${answer[i]}</h2>`;
					return;					
				}
				let ans = answer[i]["hits"]["hits"];
				for(let j=0; j<ans.length; j++){
					let source = ans[j]["_source"];					
					if(ques_class=="QTY"){
						let ingredients = [];
						source["Ingredients"].forEach((ing, index)=>{
							ing_entities.forEach((ing_entity)=>{
								if(ing.includes(ing_entity)){
									ingredients.push(ing);
								}
							});
						});
						source["Ingredients"] = ingredients;
					}													
					let output = formatAnswer(source);
					$("#answer")[0].innerHTML += output;
				}
				$("#answer")[0].innerHTML += '<br><hr></br>';
			}					
		}).fail((err)=>{
			console.log(err);
		});			
	}
});

function formatAnswer(source){
	let title = category = avatar = description = prepTime = cookTime = additionTime = totalTime 
	= serving = nutrition = instructions = ingredients = utensils = ``;
	if (source["Title"]){				
		title 		 = `<p><strong>Title</strong>: ${source["Title"]}</p>`;			
		
	}
	if (source["Category"]){
		category     = `<p><strong>Category</strong>: ${source["Category"]}</p>`;
	}
	if (source["Avatar"]){
		avatar       = `<img src="${source["Avatar"]}">`;
	}
	if (source["Description"]){
		description  = `<p><strong>Description</strong>: ${source["Description"]}</p>`;
	}
	if (source["PrepTime"]){
		prepTime     = `<p><strong>Prepare Time</strong>: ${source["PrepTime"]}</p>`;
	}
	if (source["CookTime"]){
		cookTime     = `<p><strong>Cooking Time</strong>: ${source["CookTime"]}</p>`;
	}
	if (source["AdditionTime"]){
		additionTime = `<p><strong>Additional Time</strong>: ${source["AdditionTime"]}</p>`;
	}
	if (source["TotalTime"]){
		totalTime    = `<p><strong>Total Time</strong>: ${source["TotalTime"]}</p>`;
	}
	if (source["Serving"]){
		serving      = `<p><strong>Serving</strong>: ${source["Serving"]}</p>`;
	}
	if (source["Nutrition"]){
		nutrition    = `<p><strong>Nutrition Fact</strong>: ${source["Nutrition"]}</p>`;
	}
	if (source["Instructions"]){
		let ins = source["Instructions"];
		instructions = `<ul><h4>Instructions:</h4>`;
		for(let i=0;i<ins.length;i++){
			let instruct = `<li><strong>Step ${i+1}</strong>: ${ins[i]}</li>`;
			instructions += instruct;
		}
		instructions += '</ul>';
	}
	if (source["Ingredients"]){
		let ings  = source["Ingredients"];
		ingredients = `<ul><h4>Ingredients:</h4>`;
		for(let i=0;i<ings.length;i++){
			let ing = `<li>- ${ings[i]}</li>`;
			ingredients += ing;
		}
		ingredients += '</ul>';
		
	}
	if (source["Utensils"]){
		let uts  = source["Utensils"];
		utensils = `<ul><h4>Utensils:</h4>`;
		for(let i=0;i<uts.length;i++){
			let u = `<li>- ${uts[i]}</li>`;
			utensils += u;
		}
		utensils += '</ul>';
		
	}
	let time = ``
	if (source["PrepTime"]||source["AdditionTime"]||source["CookTime"]||source["TotalTime"]){
		time = `<ul>
					<li>${prepTime}</li>
					<li>${cookTime}</li>
					<li>${additionTime}</li>
					<li>${totalTime}</li>				
				</ul>`;
	}
	output = title+category+description+serving+avatar+ingredients+utensils+time+instructions+nutrition;
	return output;
}