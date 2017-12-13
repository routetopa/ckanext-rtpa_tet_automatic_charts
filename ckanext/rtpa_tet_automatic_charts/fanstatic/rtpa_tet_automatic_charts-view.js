this.ckan.module('rtpa_tet_automatic_charts_view', function(jQuery, _) {
	return{
		initialize: function() {
            jQuery.proxyAll(this, /_on/);
            this.el.ready(this._onReady);
		},
		_onReady: function() {
			console.log("ready");
			this.renderCharts(JSON.parse(this.options.resource));
		},
		renderCharts:function(data){
			for(var i=0; i<data.length; i++){
				tempcolumndata=data[i]
				for (j=0; j<tempcolumndata.length;j++){
					/*console.log("#"+tempcolumndata[j][0])
					console.log(tempcolumndata[j][1])
					console.log(tempcolumndata[j][2]);
					var frequency=tempcolumndata[j][1];
					var valueranges=tempcolumndata[j][2];
					for (var a=0; a<frequency.length && a<valueranges.length; a++){
						console.log(frequency[a])
						console.log(valueranges[a])
					}*/

					var frequency=tempcolumndata[j][1].concat(tempcolumndata[j][0]);
					var valueranges=tempcolumndata[j][2].concat('ranges');
					console.log(frequency);
					console.log(valueranges);
					/*console.log([[tempcolumndata[j][0]]+" "+tempcolumndata[j][1]])*/
					
					c3.generate({
						bindto: "#"+tempcolumndata[j][0],
						data:{
							/*x: [valueranges[0]],*/
							columns:[
							frequency
						],
						types:{
							[frequency[0]]: 'bar' //ADD
						}
					},
					axis:{
						x:{
								type:'category',
								categories: tempcolumndata[j][2]
						}
						
					}
					});
					
					
					
					

				}
				
				
			}
		}
		
}
});
