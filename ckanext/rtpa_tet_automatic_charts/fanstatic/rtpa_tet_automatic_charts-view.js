this.ckan.module('rtpa_tet_automatic_charts_view', function(jQuery, _) {
	return{
		initialize: function() {
            jQuery.proxyAll(this, /_on/);
            this.el.ready(this._onReady);
		},
		_onReady: function() {
			console.log("ready");
			console.log(this.options.resource);
			this.renderCharts(JSON.parse(this.options.resource));
		},
		renderCharts:function(data){
			for(var i=0; i<data.length; i++){
				tempcolumndata=data[i]
				for (j=0; j<tempcolumndata.length;j++){
					console.log("#"+tempcolumndata[j][0])
					console.log(tempcolumndata[j][1])
					console.log(tempcolumndata[j][2])
				}
				
				
			}
		}
		
}
});
