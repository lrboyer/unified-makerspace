import { useState } from "react";
import StaffIn from "../components/StaffIn";
import StudentQuizProgress from "../components/StudentQuizProgress";

const StaffPortal = () => {
  const [authenticated, setAuthenticated] = useState(false);

  return (
    <>
      {authenticated ? (
        <StudentQuizProgress />
      ) : (
        <StaffIn setAuthenticated={setAuthenticated} />
      )}
    </>
  );
};
export default StaffPortal;
