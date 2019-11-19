import React, { Component } from 'react';
import { Switch, Route, BrowserRouter as Router } from 'react-router-dom'
import { Security, ImplicitCallback, SecureRoute } from '@okta/okta-react';

import Login from '../Login'
import Home from '../Home'
import Logout from '../Logout'

class Main extends Component {
 render() {
   return (
     <Router>
       <Security
         issuer={'https://dev-885573.okta.com/oauth2/default'}
         client_id={'0oa1sqdd1i125orwP357'}
         redirect_uri={'http://localhost:8080/authorization-code/callback'}
         scope={['openid', 'profile', 'email']}>

         <Switch>
           <Route exact path="/" component={Login} />
           <Route path="/authorization-code/callback" component={ImplicitCallback} />
           <SecureRoute path="/home" component={Home} />
           <SecureRoute path="/logout" component={Logout} />
         </Switch>
       </Security>
     </Router>
   );
 }
}

export default Main;
