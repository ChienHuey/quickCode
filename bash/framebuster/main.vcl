include "default"
include "backends"
include "redirects"

sub aetn_services_recv {
	call aetn_default_backend;
	call aetn_services_proxypass;
	call aetn_services_rewrites;
}

sub aetn_default_backend {

	set req.http.Fastly-Orig-Host = req.http.host;
	set req.http.host = "framebuster-devops-aetnd-com.s3.amazonaws.com";	
	
	if (req.http.AETN-env ~ "DEV") {
    	set req.http.host = "dev-framebuster-devops-aetnd-com.s3.amazonaws.com";
	}

	if (req.http.AETN-env ~ "QA") {
    	set req.http.host = "qa-framebuster-devops-aetnd-com.s3.amazonaws.com";
	}

	set req.backend = framebuster_devops_aetnd_com;
}

sub aetn_services_proxypass {

}

sub aetn_services_rewrites {

	set req.http.X-Redirect = table.lookup(redirects_301, req.url);

	if (req.http.X-Redirect) {
		error 701 req.http.X-Redirect;
	}

	set req.http.X-Redirect = table.lookup(redirects_302, req.url);

	if (req.http.X-Redirect) {
		error 702 req.http.X-Redirect;
	}
}
