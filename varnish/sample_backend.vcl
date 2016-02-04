backend s3_sample_com {
	.first_byte_timeout      = 15s;
	.connect_timeout         = 1s;
	.dynamic                 = true;
	.max_connections         = 200;
	.between_bytes_timeout   = 10s;
	.share_key               = "48zyRZcu738TH63Yo6TLvM";
	.port                    = "443";
	.host                    = "s3.amazonaws.com";

	.probe = {
    .request 	= "HEAD /iamhere.html HTTP/1.1" "Host: s3.sample.com.s3.amazonaws.com" "Connection: close";
		.interval 	= 5s;
		.timeout 	= 1s;
		.window 	= 5;
		.threshold 	= 3;
		.dummy = true;
	}
}