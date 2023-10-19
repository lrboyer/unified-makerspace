import { useState, useEffect } from "react";
import PageCard from "./PageCard";
import Footer from "../components/Footer";

const StudentQuizProgress = () => {
  const [searchUsername, setSearchUsername] = useState("");
  const [user, setUser] = useState<string | null>(null);
  const [quizzes, setQuizzes] = useState<
    {
      name: string;
      status: number;
    }[]
  >([]);
  const [loading, setLoading] = useState(false);

  const testQuizData = [
    { name: "General Safety Quiz", status: -1 },
    { name: "3D Printer Quiz (FDM)", status: 0 },
    { name: "3D Printer Quiz (SLA)", status: 1 },
    { name: "Epilog Laser Quiz", status: -1 },
    { name: "Glowforge Laser Quiz", status: 1 },
    { name: "Sticker Printer Quiz", status: 0 },
    { name: "Vinyl Cutter Quiz", status: -1 },
    { name: "Fabric Printer Quiz", status: 1 },
    { name: "Embroidery Machine/Sewing Machine Quiz", status: 0 },
    { name: "3D Scanner Quiz", status: -1 },
  ];

  const handleSearch = () => {
    // Construct the URL for your API endpoint
    const apiUrl = `YOUR_API_ENDPOINT/${searchUsername}`;

    setLoading(true);

    /*
    fetch(apiUrl)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        setQuizzes(data); // Assuming the response data is an array of quiz objects
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
        setLoading(false);
      });

    */
    setQuizzes(testQuizData);
    setUser(searchUsername);
    setLoading(false);
  };

  useEffect(() => {}, []);

  return (
    <div
      className="container bg-primary p-5 rounded d-flex flex-column"
      style={{ minHeight: "30%", maxWidth: "95%" }}
    >
      <div className="mb-4 text-center">
        <h1 className="text-secondary fw-bold mb-1">Student Quiz Progress</h1>
      </div>
      <div className="d-flex flex-column align-items-center justify-content-center text-white">
        <div className="mb-3">
          <label htmlFor="username" className="form-label">
            Search by Username:
          </label>
          <div className="input-group">
            <input
              type="text"
              className="form-control"
              id="username"
              value={searchUsername}
              onChange={(e) => setSearchUsername(e.target.value)}
            />
            <button
              className="btn btn-secondary"
              type="button"
              onClick={handleSearch}
            >
              Search
            </button>
          </div>
        </div>
        {loading ? (
          <p>Loading...</p>
        ) : (
          <table className="table table-bordered table-primary">
            <thead>
              <tr>
                <th className="text-center align-middle">Username</th>
                {quizzes.map((quiz, index) => (
                  <th className="text-center align-middle" key={index}>
                    {quiz.name}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              <tr>
                <td className="text-center align-middle">{user}</td>
                {quizzes.map((quiz, index) => (
                  <td
                    key={index}
                    className={
                      quiz.status === 1
                        ? "bg-success text-center align-middle" // Passed
                        : quiz.status === 0
                        ? "bg-danger text-center align-middle" // Failed
                        : "text-center align-middle" // Not Attempted
                    }
                  >
                    {quiz.status === 1
                      ? "Passed"
                      : quiz.status === 0
                      ? "Failed"
                      : "Not Attempted"}
                  </td>
                ))}
              </tr>
            </tbody>
          </table>
        )}
      </div>
      <div className="flex-grow-1"></div>
      <Footer />
    </div>
  );
};

export default StudentQuizProgress;
