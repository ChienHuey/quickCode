backend framebuster_devops_aetnd_com {
	.first_byte_timeout      = 3s;
	.connect_timeout         = 1s;
	.dynamic                 = true;
	.max_connections         = 200;
	.between_bytes_timeout   = 10s;
	.share_key               = "53AlG8wvz848UXwZGVFsKe";
	.port                    = "443";
	.host                    = "s3.amazonaws.com";

	.probe = {
    .request 	= "HEAD /aetn-heartbeat.html HTTP/1.1" "Host: framebuster-devops-aetnd-com.s3.amazonaws.com" "Connection: close";
		.interval 	= 5s;
		.timeout 	= 1s;
		.window 	= 5;
		.threshold 	= 3;
		.dummy = true;
	}
}
