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
					var frequency=tempcolumndata[j][1].concat(tempcolumndata[j][0]);
					var valueranges=tempcolumndata[j][2].concat('ranges');
					
					c3.generate({
						bindto: "#"+tempcolumndata[j][0],
						data:{
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
