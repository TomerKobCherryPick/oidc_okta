import React from 'react'
import Button from '@material-ui/core/Button';
import { Redirect } from 'react-router-dom'
import { withAuth } from '@okta/okta-react';

class Logout extends React.Component {
 constructor(props) {
   super(props);
 }

 render() {
     return (
       <div style={{height: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
         <Button
          variant="contained"
          color="secondary"
          onClick={() =>
             this.props.auth.logout()
           }>
           {'Logout with Okta'}
           </Button>
       </div>
     )
   }
}

export default withAuth(Logout);
