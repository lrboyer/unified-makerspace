import {Injectable} from '@angular/core';
import {HttpHandler, HttpInterceptor, HttpRequest} from '@angular/common/http';
import {AuthService} from './auth/auth.service';
import {environment} from '../../environments/environment';


@Injectable({
  providedIn: 'root',
})
export class InterceptorService implements HttpInterceptor{

  constructor(private auth: AuthService){}

  intercept(req: HttpRequest<any>, next: HttpHandler) {

    // all outgoing requests are json
    let request = req.clone({
      headers: req.headers.append('Content-Type', 'application/json')
    })



    // authenticate outgoing requests
    // if (this.auth.isUserLoggedIn()) {
    //   request = request.clone({ // all outgoing requests are json
    //     headers: req.headers.append('Authorization', this.auth.user.getValue()['auth_token'])
    //   })
    // }


    if (!environment.production) {
      // log all outgoing requests in development
      console.info(request.url, request);
    }

    return next.handle(request);
  }
}
