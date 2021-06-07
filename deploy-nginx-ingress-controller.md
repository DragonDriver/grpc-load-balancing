# deploy nginx-ingress-controller

1, nginx-ingress-controller 只支持 tls（https）访问，因此需要配置 tls secret；

```shell
$ openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout tls.key -out tls.crt -subj "/CN=greeter.demo.com"
```

2，生成 k8s secret；

```shell
$ kubectl create secret tls grpc-lb-demo-tls --key="tls.key" --cert="tls.crt"
```

