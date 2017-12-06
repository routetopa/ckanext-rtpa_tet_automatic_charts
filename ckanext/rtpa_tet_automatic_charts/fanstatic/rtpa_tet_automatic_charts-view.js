this.ckan.module('rtpa_tet_automatic_charts_view', function(jQuery, _) {
	
	return{
		initialize: function() {
            jQuery.proxyAll(this, /_on/);
            this.el.ready(this._onReady);
            },
        _onReady: function() {
			console.log(this.options.resource);
			
		}
		
}
});
